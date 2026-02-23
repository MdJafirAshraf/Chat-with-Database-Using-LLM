import sqlite3
import pandas as pd


def execute_sql(query: str) -> pd.DataFrame:
    conn = sqlite3.connect("app\\instance\\olist.sqlite")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df