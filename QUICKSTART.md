# Quick Start Guide

Get your Excel Formula Optimizer up and running in 5 minutes!

## Prerequisites

- Python 3.12+
- Anthropic API key

## Step 1: Install Dependencies

```bash
uv sync
```

## Step 2: Configure API Key

Create a `.env` file in the project root:

```bash
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

Replace `your-api-key-here` with your actual Anthropic API key from https://console.anthropic.com/

## Step 3: Run the Application

**Option A: Use the quick start script**

```bash
./run.sh
```

**Option B: Run manually**

```bash
# Terminal 1: Start backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start frontend
python3 -m http.server 8080 --directory frontend
```

## Step 4: Test It Out

1. Open your browser to `http://localhost:8080`
2. Enter a formula like: `=IF(A1>0,IF(B1<10,"OK","NO"),"FAIL")`
3. Click "Beautify" to see the formatted version
4. Click "Simplify with AI" to get an optimized version with explanation

## API Testing

You can also test the API directly:

**Swagger UI**: http://localhost:8000/docs

**Example API call**:

```bash
curl -X POST "http://localhost:8000/format" \
  -H "Content-Type: application/json" \
  -d '{"formula": "=IF(A1>0,\"Yes\",\"No\")"}'
```

## Run Tests

```bash
pytest tests/ -v
```

## Troubleshooting

- **API key error**: Make sure `.env` file exists and contains valid `ANTHROPIC_API_KEY`
- **Port in use**: Change port numbers in the commands above
- **Dependencies error**: Run `uv sync` again

## Example Formulas

Try these formulas to test the optimizer:

```
=IF(A1>0,IF(B1<10,"OK","NO"),"FAIL")
=VLOOKUP(A1,Sheet2!A:B,2,FALSE)
=SUMIFS(D:D,A:A,">=2023",B:B,"Sales")
=IF(AND(A1>0,B1<10,C1="Active"),"Valid","Invalid")
```

## Next Steps

- Check out `README.md` for full documentation
- See `CLAUDE.md` for development guidelines
- Explore the API docs at http://localhost:8000/docs
