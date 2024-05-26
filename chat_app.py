import gradio as gr
from local_chat_memory import chat, preload


# ChatInterface (gradio) -> {query, history} -> our_function
# our_function -> {response} -> ChatInterface (gradio)


def run_gradio_chat(query, _):
    response = chat(query, gradio_mode=True)
    full_message = ""
    if response:
        for chunk in response:
            full_message += chunk
            yield full_message
    else:
        yield "There was an error fetching the response. Please try again."


if __name__ == "__main__":
    preload()
    gr.ChatInterface(
        run_gradio_chat, retry_btn=None, undo_btn=None, clear_btn=None
    ).launch()
