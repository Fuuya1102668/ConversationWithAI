from langchain_community.llms import LlamaCpp
from llama_cpp import Llama
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

model = LlamaCpp(
    model_path="models/marged_model/ggml-model-Q4_K.gguf",
    n_gpu_layers=-1,
    f16_kv=True,
    verbose=True,
    )

config = {"configurable": {"session_id": "zunda"}}

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in japanese.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | model

response = chain.invoke({"messages": [HumanMessage(content="hi! I'm fuya.")]})

#response.content
print(response)

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
)

response = with_message_history.invoke(
    [HumanMessage(content="whats my name?")],
    config=config,
)

#chain = prompt | model
#
#response = chain.invoke(
#    {"messages": [HumanMessage(content="hi! I'm bob")], "language": "japanese"}
#)
#
#response.content
print(response)

