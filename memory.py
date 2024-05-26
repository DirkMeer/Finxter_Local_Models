from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel, Field


class LimitedHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of limited chat message history storing only the last K messages."""

    messages: list[BaseMessage] = Field(default_factory=list)
    max_messages: int = 10

    def add_messages(self, messages: list[BaseMessage]) -> None:
        self.messages.extend(messages)
        self.messages = self.messages[-self.max_messages :]

    def clear(self) -> None:
        self.messages = []
