import re
from fastapi import HTTPException
from app.core.llm import run_prompt
from app.core.prompts import (
    SQL_SYSTEM_PROMPT,
    ANSWER_SYSTEM_PROMPT
)
from app.database.db import execute_sql
from app.database.security import is_safe_sql


def question_to_sql(question: str) -> str:
    '''
    Convert a natural language question into an SQL query using a language model.
    The function takes a question as input, runs it through a prompt to generate SQL,
    and then cleans the output to extract the SQL query.

    Args:
        question (str): The natural language question to be converted into SQL.
    
    Returns:
        str: The generated SQL query.
    '''
    try:
        sql = run_prompt(SQL_SYSTEM_PROMPT, question)
        clean_sql = re.sub(r"```sql|```", "", sql).strip()
        print(f"Generated SQL: {clean_sql}")
        return clean_sql
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating SQL: {str(e)}")


def dataframe_to_answer(df):
    '''
    Convert a DataFrame result into a natural language answer using a language model.

    Args:        
        df (pd.DataFrame): The DataFrame result from executing an SQL query.

    Returns:
        str: The generated natural language answer based on the DataFrame content.
    '''
    if df.empty:
        return "No data found."

    return run_prompt(
        ANSWER_SYSTEM_PROMPT,
        df.to_string(index=False)
    )


def handle_question(question: str):
    '''
    Handle a natural language question by converting it to SQL, executing the SQL query,
    and converting the result into a natural language answer.

    Args:
        question (str): The natural language question to be processed.

    Returns:
        dict: A dictionary containing the original question, the generated SQL query, and the final answer
    '''
    # Convert the natural language question into an SQL query
    sql = question_to_sql(question)

    # Check if the generated SQL query is safe before executing it
    if not is_safe_sql(sql):
        return {
            "question": question,
            "sql": sql,
            "error": "The generated SQL query is not safe to execute."
        }

    # Execute the SQL query and get the result as a DataFrame
    try:
        df = execute_sql(sql)
        print(f"SQL Execution Result:\n{df}")
    except:
        return {
            "question": question,
            "sql": '',
            "answer": sql
        }
    
    # Convert the DataFrame result into a natural language answer
    answer = dataframe_to_answer(df)
    print(f"Generated Answer: {answer}")

    return {
        "question": question,
        "sql": sql,
        "answer": answer
    }