import sqlite3
import pandas as pd

DB_PATH = "app/instance/olist.sqlite"

def execute_sql(sql: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def is_safe_sql(sql: str) -> bool:
    forbidden = ["delete", "drop", "update", "insert", "alter", "truncate"]
    sql_lower = sql.lower()
    return not any(word in sql_lower for word in forbidden)
