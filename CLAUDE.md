# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An AI-powered web application that beautifies and optimizes Excel formulas. Users can input complex Excel formulas and receive:
1. A human-readable formatted version with proper indentation (that still works in Excel)
2. An AI-generated optimized/simplified version using modern Excel functions
3. An explanation of the improvements made

The project uses FastAPI for the backend and vanilla HTML/JS for the frontend with a liquid glass design aesthetic.

## Environment Setup

**Python Version**: Requires Python >=3.12

**Package Management**: This project uses `uv` for dependency management.

### Installation Commands

```bash
# Install dependencies
uv pip install -r requirements.txt

# Or sync from pyproject.toml
uv sync
```

### Environment Variables

The project requires API keys configured in `.env`:
- `OPENAI_API_KEY` - For OpenAI services
- `ANTHROPIC_API_KEY` - For Anthropic/Claude services

**IMPORTANT**: Never commit the `.env` file. API keys are sensitive credentials.

## Architecture & Key Dependencies

This project integrates multiple AI agent frameworks and services:

### Agent Frameworks
- **AutoGen** (autogen-agentchat, autogen-core, autogen-ext): Multi-agent conversation framework with gRPC, MCP, and Ollama extensions
- **LangChain/LangGraph**: Agent orchestration with Anthropic, OpenAI, and experimental features
  - Uses SQLite checkpointing for state persistence
- **Semantic Kernel**: Microsoft's AI orchestration SDK
- **OpenAI Agents**: OpenAI's native agent framework

### AI Service Integration
- **Anthropic**: Claude API integration via langchain-anthropic
- **OpenAI**: GPT models and agents
- **Ollama**: Local LLM support

### MCP (Model Context Protocol)
- MCP server support with CLI
- mcp-server-fetch for web content retrieval
- Used for extending agent capabilities with external tools/context

### Additional Capabilities
- **Gradio**: Web UI framework (likely for agent interfaces)
- **Playwright**: Browser automation
- **Web scraping**: BeautifulSoup4, lxml, readabilipy
- **PDF processing**: pypdf, pypdf2
- **Data processing**: pandas, numpy, plotly
- **API clients**: polygon-api-client (financial data), wikipedia, sendgrid

## Development Workflow

### Running the Application

```bash
# Start the FastAPI backend server
uvicorn app.main:app --reload --port 8000

# Open frontend/index.html in a browser or serve with:
python -m http.server 8080 --directory frontend
```

### Running Tests

```bash
pytest tests/
```

### API Documentation
Once running, FastAPI auto-generates docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

### Backend Structure (`app/`)
- **main.py**: FastAPI application with two main endpoints:
  - `POST /format`: Accepts formula, returns beautified version
  - `POST /simplify`: Accepts formula, returns beautified + optimized versions with explanation
- **beautifier.py**: Formula parsing and formatting logic
  - Handles indentation for nested expressions
  - Line breaks for function arguments (IF/AND/OR/LET/IFS, etc.)
  - Returns original formula if parsing fails
- **ai_agent.py**: Claude API integration for formula optimization
  - Prompts Claude to suggest modern Excel alternatives
  - Prompts Claude to suggest simplification of formula, e.g. IFS instead of multiple nested IF
  - Handles API failures gracefully
  - Returns explanation of optimizations
- **utils.py**: Common helpers and error handling

### Frontend Structure (`frontend/`)
- **index.html**: Liquid glass styled UI with:
  - Formula input textarea
  - "Beautify" and "Simplify" buttons
  - Results display with copy functionality
- **app.js**: API communication and UI updates

### AI Agent Strategy
Uses **Anthropic's Claude** (via anthropic package) for formula optimization:
- Simple, single-turn conversation for each formula
- Prompt engineering focuses on modern Excel best practices
- No complex state management needed (stateless optimization requests)

### Formula Handling
The beautifier supports common Excel functions:
- Logical: IF, IFS, AND, OR, NOT, XOR
- Lookup: VLOOKUP, HLOOKUP, INDEX, MATCH, XLOOKUP
- Aggregation: SUM, SUMIF, SUMIFS, COUNT, COUNTIF, COUNTIFS, AVERAGE
- Text: CONCATENATE, TEXTJOIN, LEFT, RIGHT, MID
- Modern: LET, LAMBDA, FILTER, SORT, UNIQUE

### Error Handling
- Invalid formula syntax: Return original with error message
- AI API failures: Fallback to beautified version only
- Empty input: Return validation error
- All errors returned with informative messages to frontend
