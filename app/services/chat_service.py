import re
from app.core.llm import run_prompt
from app.core.prompts import (
    SQL_SYSTEM_PROMPT,
    ANSWER_SYSTEM_PROMPT
)
from app.database.db import execute_sql
from app.database.security import is_safe_sql


def clean_sql(sql: str) -> str:
    return re.sub(r"```sql|```", "", sql).strip()


def question_to_sql(question: str) -> str:
    sql = run_prompt(SQL_SYSTEM_PROMPT, question)
    return clean_sql(sql)


def dataframe_to_answer(df):
    if df.empty:
        return "No data found."

    return run_prompt(
        ANSWER_SYSTEM_PROMPT,
        df.to_string(index=False)
    )


def handle_question(question: str):
    sql = question_to_sql(question)

    if not is_safe_sql(sql):
        return {"error": "Unsafe SQL detected"}

    df = execute_sql(sql)
    answer = dataframe_to_answer(df)

    return {
        "question": question,
        "sql": sql,
        "answer": answer
    }