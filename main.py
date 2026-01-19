from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import sqlite3
import pandas as pd
import re

# ------------------ CONFIG ------------------
DB_PATH = "data.db"
MODEL_PATH = "models/qwen2.5-1.5b-instruct-q4_k_m.gguf"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_threads=8
)

app = FastAPI(title="Chat with Database (Local AI)")

# ------------------ REQUEST ------------------
class QueryRequest(BaseModel):
    question: str

# ------------------ SQL SAFETY ------------------
def is_safe_sql(sql: str) -> bool:
    forbidden = ["delete", "drop", "update", "insert", "alter"]
    return not any(word in sql.lower() for word in forbidden)

# ------------------ NL → SQL ------------------
def generate_sql(question: str) -> str:
    prompt = f"""
You are an expert SQLite SQL generator.
Generate ONLY a SELECT query.
Do NOT explain anything.

Table: sales(id, product, quantity, price, date)

User question:
{question}

SQL:
"""
    output = llm(prompt, max_tokens=200)
    sql = output["choices"][0]["text"].strip()
    sql = re.sub(r"```sql|```", "", sql).strip()
    return sql

# ------------------ RUN SQL ------------------
def run_query(sql: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

# ------------------ RESULT → TEXT ------------------
def explain_result(df: pd.DataFrame) -> str:
    if df.empty:
        return "No data found for your query."

    prompt = f"""
Explain this data in simple business language:

{df.to_string(index=False)}
"""
    output = llm(prompt, max_tokens=200)
    return output["choices"][0]["text"].strip()

# ------------------ API ------------------
@app.post("/chat")
def chat(request: QueryRequest):
    sql = generate_sql(request.question)

    if not is_safe_sql(sql):
        return {"error": "Unsafe SQL detected"}

    df = run_query(sql)
    answer = explain_result(df)

    return {
        "question": request.question,
        "sql": sql,
        "answer": answer
    }
