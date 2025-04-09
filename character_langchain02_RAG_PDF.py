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
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PDFMinerLoader
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import requests
import json
import getapi, os

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def create_openai_model(model_name):
    text_model = ChatOpenAI(
        model=model_name,
        streaming=True
    )
    return text_model

def ollama_model(model_name, prompt, host, port="11434"):
    url = "http://"+host+":"+port+"/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    result = response.json()

    return result.get("response", "")

def loade_pdf(directory, file):
    loader = DirectoryLoader(directory, glob=file)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    return retriever

def create_chain(text_model, retriever, contextualize_q_system_prompt, qa_system_prompt):
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
            ("system", qa_system_prompt,),
            MessagesPlaceholder("chat_history"),
            ("human","{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(text_model, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
        )
    return conversational_rag_chain

def add_history(chat_history, inputs, outputs):
    chat_history.extend(
        [
            HumanMessage(content=inputs),
            AIMessage(content=outputs["answer"]),
        ]
    )
    return chat_history

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = getapi.get_api()
    config = {"configurable": {"session_id": "zunda"}}
    #model_name = "gpt-3.5-turbo-0125:personal::9ol99gYa"
    model_name = "ft:gpt-4o-mini-2024-07-18:personal::9xnTRBnP"
    directory = "./rag_source"
    file = "*.pdf"
    contextualize_q_system_prompt = (
        "チャット履歴と，チャット履歴のコンテキストを参照する可能性のある最新のユーザの質問が与えられた場合，チャット履歴無しで理解できる独立した質問を作成してください．質問には答えず，必要であれば再作成し，そうでなければそのまま返します．"
    )
    qa_system_prompt = "あなたの名前はずんだもんです．語尾は「なのだ」または「のだ」です．例えば「こんにちは」は「こんにちはなのだ」になります．また，「よろしくお願いします」は「よろしくお願いするのだ」になります．これからはすべて日本語で回答してください．また，回答は必ず，contextを参照してから行ってください．{context}"

    text_model = create_openai_model(model_name)
    retriever = loade_pdf(directory, file)
    conversational_rag_chain = create_chain(text_model, retriever, contextualize_q_system_prompt, qa_system_prompt)

    try:
        with open("history_" + config["configurable"]["session_id"] + ".plk", "rb") as f:
            chat_history = pickle.load(f)
    except FileNotFoundError:
        chat_history = []
    while True:
        outputs = ""
        inputs = input("  あなた  ：")
        if inputs.lower() == "exit":
            break
        outputs = conversational_rag_chain.invoke(
            {"input":inputs},
            config=config,
            )
        chat_history = add_history(chat_history, inputs, outputs)   
        print("ずんだもん：", outputs["answer"])

    with open("history_" + config + ".plk", "wb") as f:
        pickle.dump(my_list, f)
    print("ずんだもん：会話内容を保存したのだ．また今度なのだ．")

