from langchain_community.llms import LlamaCpp
from llama_cpp import Llama
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

import getapi, os
import sounddevice as sd
import bs4
import requests
from pydub import AudioSegment
from pydub.playback import play
import io

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

url = "http://127.0.0.1:5000/voice"
headers = {"accept": "audio/wav"}
params = {
    "text":"",
    "encodeng":"utf-8",
    "model_name":"zundamon",
}

os.environ["OPENAI_API_KEY"] = getapi.get_api()

store = {}

config = {"configurable": {"session_id": "zunda"}}

text_model = ChatOpenAI(model="ft:gpt-3.5-turbo-0125:personal::9ol99gYa")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "これからはすべて日本語で回答してください．あなたの名前はずんだもんです．語尾は「なのだ」または「のだ」です．例えば「こんにちは」は「こんにちはなのだ」になります．また，「よろしくお願いします」は「よろしくお願いするのだ」になります．ずんだもんはずんだの妖精で，JTCで働いているpythonのエンジニアです．",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | text_model

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
)

while True:
    inputs = input("  あなた  ：")
    outputs = with_message_history.invoke(
        [HumanMessage(content=inputs)],
        config=config,
    )
    print("ずんだもん：" + outputs.content)

