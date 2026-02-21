from langchain_cerebras import ChatCerebras
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings


def run_prompt(system_prompt: str, user_input: str) -> str:

    llm = ChatCerebras(
        cerebras_api_key=settings.CEREBRAS_API_KEY,
        model="llama3.1-8b",
        temperature=0.2,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"input": user_input})