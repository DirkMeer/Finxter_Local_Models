import uuid
import threading
from typing import Iterator

from langchain_community.llms import Ollama
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from model_preloader import preload_model
from memory import LimitedHistory


store = {}
HISTORY_LIMIT = 4
MODEL_NAME = "llama3"
LLAMA3 = Ollama(model=MODEL_NAME)
SYSTEM_MESSAGE = "You are a wise Jedi Master and helpful assistant. Your name is Yoda and you will address the user as Obi-Wan Kenobi at all times."
SESSION_ID = uuid.uuid4()


prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_MESSAGE),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{query}"),
    ]
)


llama3_chain = prompt_template | LLAMA3


def get_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = LimitedHistory(max_messages=HISTORY_LIMIT)
    return store[session_id]


llama3_w_memory = RunnableWithMessageHistory(
    llama3_chain,
    get_history,
    input_messages_key="query",
    history_messages_key="history",
)


def chat(query: str, gradio_mode: bool = False) -> None | Iterator[str]:
    response = llama3_w_memory.stream(
        {"query": query}, config={"configurable": {"session_id": SESSION_ID}}
    )
    if gradio_mode:
        return response
    else:
        for chunk in response:
            print(chunk, end="")


def preload(model_name: str = MODEL_NAME) -> None:
    thread = threading.Thread(target=preload_model, args=[model_name])
    thread.start()


if __name__ == "__main__":
    preload()
    try:
        while True:
            query = input("You: ")
            chat(query)
            print("\n")
    except KeyboardInterrupt:
        print("Shutting down...")
