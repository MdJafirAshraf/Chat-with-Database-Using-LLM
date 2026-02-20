import re
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from langchain_groq import Groq
from pydantic import BaseModel
from app.core.prompts import SQL_PROMPT, ANSWER_PROMPT
from app.database import execute_sql, is_safe_sql

app = FastAPI(title="Chat with Local Database AI")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

MODEL_PATH = r"app\models\Phi-3-mini-4k-instruct-q4.gguf"

llm = Groq(model=MODEL_PATH, temperature=0.2)

class ChatRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
def chat(request: ChatRequest):
    return handle_question(request.question)


def run_llm(prompt: str, max_tokens: int = 256) -> str:
    # LangChain wrappers may return a plain string, a dict (legacy),
    # or an LLMResult-like object with `.generations`.
    result = llm(prompt, max_tokens=max_tokens)
    if isinstance(result, str):
        return result.strip()
    if isinstance(result, dict):
        return result.get("choices", [{}])[0].get("text", "").strip()
    # Try LLMResult-style access
    try:
        return result.generations[0][0].text.strip()
    except Exception:
        return str(result).strip()


def question_to_sql(question: str) -> str:
    prompt = SQL_PROMPT.format(question=question)
    sql = run_llm(prompt)
    sql = re.sub(r"```sql|```", "", sql).strip()
    return sql


def dataframe_to_text(df):
    if df.empty:
        return "No data found for your query."

    prompt = ANSWER_PROMPT.format(table=df.to_string(index=False))
    return run_llm(prompt)


def handle_question(question: str):
    sql = question_to_sql(question)

    if not is_safe_sql(sql):
        return {"error": "Unsafe SQL detected"}

    df = execute_sql(sql)
    answer = dataframe_to_text(df)

    return {
        "question": question,
        "sql": sql,
        "answer": answer
    }

