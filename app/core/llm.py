from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings


def get_llm(provider: str):
    if provider == "groq":
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name="llama3-70b-8192",
            temperature=0.2
        )

    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            google_api_key=settings.GOOGLE_API_KEY,
            model="gemini-1.5-flash",
            temperature=0.2
        )

    else:
        raise ValueError("Unsupported LLM provider")


def run_prompt(provider: str, system_prompt: str, user_input: str) -> str:
    llm = get_llm(provider)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"input": user_input})