from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama

LLAMA3 = Ollama(model="llama3")
SYSTEM_MESSAGE = "You are a helpful assistant. Your name is Luigi and you will address the user as Mario at all times."


prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_MESSAGE),
        ("human", "{query}"),
    ]
)

llama3_chain = prompt_template | LLAMA3 | StrOutputParser()


def chat(query: str) -> None:
    for chunk in llama3_chain.stream(query):
        print(chunk, end="")


if __name__ == "__main__":
    while True:
        query = input("You: ")
        chat(query)
        print("\n")
