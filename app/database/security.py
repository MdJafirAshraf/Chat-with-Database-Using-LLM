import re

def is_safe_sql(query: str) -> bool:
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]
    pattern = re.compile(r"\b(" + "|".join(forbidden) + r")\b", re.IGNORECASE)
    return not bool(pattern.search(query))