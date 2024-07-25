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
from style_bert_vits2.nlp import bert_models
from style_bert_vits2.constants import Languages
from pathlib import Path
from style_bert_vits2.tts_model import TTSModel
import sounddevice as sd
import voice

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

assets_root = Path("../Style-Bert-VITS2/model_assets/zundamon/")
model_file = assets_root / "zundamon_e100_s16200.safetensors"
config_file = assets_root / "config.json"
style_file = assets_root / "style_vectors.npy"
voice_model = voice.load_model(model_file=model_file, config_file=config_file, style_file=style_file)

os.environ["OPENAI_API_KEY"] = getapi.get_api()

store = {}

config = {"configurable": {"session_id": "zunda"}}

text_model = ChatOpenAI(model="gpt-3.5-turbo")

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
    response = with_message_history.invoke(
        [HumanMessage(content=inputs)],
        config=config,
    )

    sr, audio = voice_model.infer(text=response.content)
    print("ずんだもん：" + response.content)
    sd.play(audio, sr)
    sd.wait()

