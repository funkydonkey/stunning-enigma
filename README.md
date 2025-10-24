# Excel Formula Optimizer

An AI-powered web application that beautifies and optimizes Excel formulas using Claude AI.

## Features

- 🎨 **Beautify**: Format Excel formulas with proper indentation and line breaks for readability
- 🤖 **AI Optimization**: Get suggestions for simplified and modernized formulas using Claude
- 💡 **Explanations**: Understand what improvements were made and why
- 🎭 **Beautiful UI**: Liquid glass design aesthetic for a modern look
- 📋 **Copy to Clipboard**: Easy copying of formatted formulas

## Screenshots

Enter any Excel formula and get both beautified and optimized versions with explanations.

## Tech Stack

- **Backend**: FastAPI (Python 3.12+)
- **AI**: Anthropic's Claude 3.5 Sonnet
- **Frontend**: Vanilla HTML/CSS/JavaScript with liquid glass styling
- **Package Manager**: uv

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Anthropic API key ([get one here](https://console.anthropic.com/))

## Installation

1. **Clone or download this repository**

2. **Install dependencies using uv**

```bash
# Install dependencies
uv sync
```

3. **Set up environment variables**

Create a `.env` file in the project root:

```bash
ANTHROPIC_API_KEY=your-api-key-here
```

**Important**: Never commit your `.env` file to version control!

## Running the Application

### Start the Backend Server

```bash
# Activate virtual environment (if not already activated)
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Run the FastAPI server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Access API Documentation

FastAPI provides interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Open the Frontend

You can either:

**Option 1**: Open directly in browser
```bash
open frontend/index.html
```

**Option 2**: Serve with Python's HTTP server
```bash
python -m http.server 8080 --directory frontend
```

Then navigate to `http://localhost:8080`

## Usage

1. **Enter a formula**: Type or paste your Excel formula into the input field
   - Example: `=IF(AND(A1>0,B1<10),"OK","FAIL")`

2. **Beautify**: Click the "Beautify" button to get a formatted version with proper indentation

3. **Simplify with AI**: Click "Simplify with AI" to get:
   - Beautified version
   - AI-optimized version using modern Excel functions
   - Explanation of the improvements

4. **Copy results**: Use the "Copy" buttons to copy formatted formulas to your clipboard

## Example Formulas to Try

```excel
=IF(A1>0,IF(B1<10,"OK","NO"),"FAIL")

=VLOOKUP(A1,Sheet2!A:B,2,FALSE)

=SUMIFS(D:D,A:A,">=2023",B:B,"Sales")

=IF(AND(A1>0,B1<10,C1="Active"),"Valid","Invalid")

=INDEX(Sheet2!B:B,MATCH(A1,Sheet2!A:A,0))
```

## API Endpoints

### POST /format
Beautify a formula with proper formatting.

**Request:**
```json
{
  "formula": "=IF(A1>0,\"Yes\",\"No\")"
}
```

**Response:**
```json
{
  "pretty": "=IF(\n    A1>0,\n    \"Yes\",\n    \"No\"\n)"
}
```

### POST /simplify
Beautify and optimize a formula with AI.

**Request:**
```json
{
  "formula": "=IF(A1>0,IF(B1<10,\"OK\",\"NO\"),\"FAIL\")"
}
```

**Response:**
```json
{
  "pretty": "=IF(\n    A1>0,\n    IF(\n        B1<10,\n        \"OK\",\n        \"NO\"\n    ),\n    \"FAIL\"\n)",
  "simplified": "=IFS(AND(A1>0,B1<10),\"OK\",A1>0,\"NO\",TRUE,\"FAIL\")",
  "comment": "Replaced nested IF statements with IFS function for better readability and reduced nesting complexity."
}
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_beautifier.py -v
```

## Project Structure

```
excel_agent/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application and endpoints
│   ├── beautifier.py     # Formula formatting logic
│   ├── ai_agent.py       # Claude AI integration
│   └── utils.py          # Utility functions
├── frontend/
│   ├── index.html        # Web UI
│   └── app.js            # Frontend logic
├── tests/
│   ├── __init__.py
│   ├── test_beautifier.py
│   ├── test_utils.py
│   └── test_api.py
├── .env                  # Environment variables (not committed)
├── pyproject.toml        # Project dependencies
├── README.md
└── CLAUDE.md            # Development guide for AI assistants
```

## Supported Excel Functions

The beautifier recognizes and formats these function types:

- **Logical**: IF, IFS, AND, OR, NOT, XOR, SWITCH, CHOOSE
- **Lookup**: VLOOKUP, HLOOKUP, XLOOKUP, INDEX, MATCH
- **Aggregation**: SUM, SUMIF, SUMIFS, COUNT, COUNTIF, COUNTIFS, AVERAGE, AVERAGEIF, AVERAGEIFS
- **Modern**: LET, LAMBDA, FILTER, SORT, SORTBY, UNIQUE

## How It Works

### Beautifier

The beautifier uses a recursive descent parser to:
1. Parse the formula into a tree structure
2. Identify function calls and arguments
3. Apply indentation rules for nested functions
4. Handle string literals and parentheses correctly
5. Format multi-line functions for readability

### AI Optimization

The AI agent:
1. Receives the original and beautified formula
2. Sends a structured prompt to Claude
3. Asks for modernization suggestions (e.g., IFS instead of nested IF)
4. Returns the optimized formula with explanation

## Troubleshooting

### API Key Issues

If you see errors about missing API keys:
1. Verify `.env` file exists in project root
2. Check `ANTHROPIC_API_KEY` is set correctly
3. Ensure no extra spaces or quotes around the key

### CORS Errors

If the frontend can't connect to the backend:
1. Verify backend is running on port 8000
2. Check `API_BASE_URL` in `frontend/app.js` matches your setup
3. Ensure CORS middleware is configured in `app/main.py`

### Formula Not Beautifying

If beautification returns the original formula:
1. Check for balanced parentheses
2. Verify the formula is valid Excel syntax
3. Look at browser console for error messages

## Development

### Adding New Features

See `CLAUDE.md` for detailed development guidance.

### Code Style

- Backend: Python type hints, docstrings for all functions
- Frontend: JSDoc comments for functions
- Tests: Pytest with descriptive test names

## License

This is a personal pet project. Feel free to use and modify as needed.

## Contributing

This is a personal project, but suggestions and improvements are welcome!

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Anthropic's Claude](https://www.anthropic.com/)
- Inspired by the need for more readable Excel formulas
