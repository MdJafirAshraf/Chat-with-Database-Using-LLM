# Chat-with-Database-Using-LLM
Chat with a local database using an LLM that converts natural language questions into safe SQL queries and returns human-readable answers via FastAPI.

## Prerequisites
- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager (faster alternative to pip)

## Installation & Setup using uv

### 1. Clone or navigate to the project directory
```cmd
cd path\to\Chat-with-Database-Using-LLM
```

### 2. Install dependencies using uv
```cmd
uv pip install -r requirements.txt
```

### 3. Create a virtual environment (optional but recommended)
```cmd
uv venv
```

Then activate the virtual environment:
```cmd
.venv\Scripts\activate
```

## Running the Project

### Start the FastAPI server
```cmd
uv run uvicorn main:app --reload
```

Or if using a virtual environment:
```cmd
.venv\Scripts\activate
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

### API Endpoints

**POST** `/chat` - Chat with the database
```json
{
  "question": "What is the average price of products?"
}
```

### Interactive API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## How It Works
1. User asks a natural language question
2. LLM converts the question to a safe SQL query
3. SQL query is validated for safety (prevents DELETE, DROP, UPDATE, etc.)
4. Query executes against the SQLite database
5. Results are converted back to human-readable text by the LLM

## Features
- ✅ Natural language to SQL conversion
- ✅ SQL injection protection
- ✅ Local LLM inference (no API calls)
- ✅ Interactive API documentation
