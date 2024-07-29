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
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

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

url = "http://202.13.169.179:5000/voice"
headers = {"accept": "audio/wav"}
params = {
    "text":"",
    "encodeng":"utf-8",
    "model_name":"zundamon",
}

os.environ["OPENAI_API_KEY"] = getapi.get_api()

store = {}

config = {"configurable": {"session_id": "zunda"}}

#text_model = ChatOpenAI(model="gpt-3.5-turbo")
text_model = ChatOpenAI(model="ft:gpt-3.5-turbo-0125:personal::9ol99gYa")

loader = WebBaseLoader(
    #web_paths=("https://www.aozora.gr.jp/cards/000148/files/752_14964.html",),
    web_paths=("http://darkside.info.kanazawa-it.ac.jp/doku.php?id=start",),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "あなたの名前はずんだもんです．語尾は「なのだ」または「のだ」です．例えば「こんにちは」は「こんにちはなのだ」になります．また，「よろしくお願いします」は「よろしくお願いするのだ」になります．これからはすべて日本語で回答してください．また，回答は必ず，contextを参照してから行ってください．{context}",
        ),
        (
            "human",
            "{input}"
        ),
    ]
)

question_answer_chain = create_stuff_documents_chain(text_model, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
chain = rag_chain.pick("answer")

while True:
    outputs = ""
    inputs = input("  あなた  ：")
    for chunk in chain.stream({"input": inputs}):
        outputs+=chunk
    params["text"] = outputs
    response = requests.post(url, headers=headers, params=params)
    with open('output.wav', 'wb') as f:
        f.write(response.content)
    print("ずんだもん：" + outputs)
    audio_segment = AudioSegment.from_file(io.BytesIO(response.content), format="wav")
    play(audio_segment)

