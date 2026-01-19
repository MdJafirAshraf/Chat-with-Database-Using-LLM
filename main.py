import re
from fastapi import FastAPI
from llama_cpp import Llama
from pydantic import BaseModel
from app.prompts import SQL_PROMPT, ANSWER_PROMPT
from app.database import execute_sql, is_safe_sql

app = FastAPI(title="Chat with Local Database AI")

MODEL_PATH = "app\models\qwen2.5-1.5b-instruct-q4_k_m.gguf"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4,
    max_tokens = 64,
    verbose=False
)


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(request: ChatRequest):
    return handle_question(request.question)


def run_llm(prompt: str, max_tokens: int = 256) -> str:
    output = llm(prompt, max_tokens=max_tokens)
    return output["choices"][0]["text"].strip()


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

