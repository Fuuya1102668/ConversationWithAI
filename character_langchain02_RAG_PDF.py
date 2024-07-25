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
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PDFMinerLoader
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

#text_model = ChatOpenAI(model="gpt-3.5-turbo")
text_model = ChatOpenAI(model="ft:gpt-3.5-turbo-0125:personal::9ol99gYa")

loader = PDFMinerLoader("stu.pdf")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

contextualize_q_system_prompt = (
    "チャット履歴と，チャット履歴のコンテキストを参照する可能性のある最新のユーザの質問が与えられた場合，チャット履歴無しで理解できる独立した質問を作成してください．質問には答えず，必要であれば再作成し，そうでなければそのまま返します．"
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human","{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    text_model, retriever, contextualize_q_prompt
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "あなたの名前はずんだもんです．語尾は「なのだ」または「のだ」です．例えば「こんにちは」は「こんにちはなのだ」になります．また，「よろしくお願いします」は「よろしくお願いするのだ」になります．これからはすべて日本語で回答してください．また，回答は必ず，contextを参照してから行ってください．{context}",
        ),
        MessagesPlaceholder("chat_history"),
        ("human","{input}"),
    ]
)

#question_answer_chain = create_stuff_documents_chain(text_model, prompt)
#rag_chain = create_retrieval_chain(retriever, question_answer_chain)
question_answer_chain = create_stuff_documents_chain(text_model, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
#chain = rag_chain.pick("answer")

chat_history = []
while True:
    outputs = ""
    inputs = input("  あなた  ：")
    outputs = rag_chain.invoke({"input":inputs, "chat_history": chat_history})
    chat_history.extend(
        [
            HumanMessage(content=inputs),
            AIMessage(content=outputs["answer"]),
        ]
    )
    params["text"] = outputs["answer"]
    response = requests.post(url, headers=headers, params=params)
    with open('output.wav', 'wb') as f:
        f.write(response.content)
    print("ずんだもん：", outputs["answer"])
    audio_segment = AudioSegment.from_file(io.BytesIO(response.content), format="wav")
    play(audio_segment)

