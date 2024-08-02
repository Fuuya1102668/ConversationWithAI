import character_langchain02_RAG_PDF as rag
import text2speech as t2s
import getapi as get
import pickle
import os

import io
import simpleaudio as sa

import socket

os.environ["OPENAI_API_KEY"] = get.get_api()
slave_ip = get.get_slave_ip()
slave_port = int(get.get_slave_port())
master_port = int(get.get_master_port())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", master_port))
s.listen(1)
conn, addr = s.accept()

config = {"configurable": {"session_id": "zunda"}}
model_name = "ft:gpt-3.5-turbo-0125:personal::9ol99gYa"
directory = "./rag_source"
file = "*.pdf"
# ここは触らない
contextualize_q_system_prompt = (
    "チャット履歴と，チャット履歴のコンテキストを参照する可能性のある最新のユーザの質問が与えられた場合，チャット履歴を優先的に参照して質問に答えてください．"
)
# ここにBotのプロンプトを書く．
qa_system_prompt = "あなたの名前はずんだもんです．これからはすべて日本語で回答してください．また，回答は必ず，contextとhistoryを参照してから行ってください．{context}"

# テキストモデルの呼び出し
text_model = rag.create_chat_model(model_name)
# pdfファイルの読み込み
retriever = rag.loade_pdf(directory, file)
# chainの作成
conversational_rag_chain = rag.create_chain(text_model, retriever, contextualize_q_system_prompt, qa_system_prompt)

try:
    with open("history_" + config["configurable"]["session_id"] + ".plk", "rb") as f:
        chat_history = pickle.load(f)
except FileNotFoundError:
    chat_history = []
print("System startup is complete.")

while True:
    outputs = ""
    inputs = s.recv(1000000)
    inputs = inputs.decode()
    print("inputs : " + str(inputs))
    if inputs.lower() == "exit":
        break
    outputs = conversational_rag_chain.invoke(
        {"input":inputs},
        config=config,
        )
    chat_history = rag.add_history(chat_history, inputs, outputs)
    response = t2s.generate_speech(outputs["answer"])
    response = pickle.dumps(response.content)
    print(len(response))
    s.sendall(response)
    print("done")
    #print("ずんだもん：", outputs["answer"])
    #sa.WaveObject.from_wave_file(io.BytesIO(response.content)).play()
    #audio_segment = AudioSegment.from_file(io.BytesIO(response.content),foemat="wav")
    #play(audio_segment)
    #print(chat_history)

with open("history_" + config["configurable"]["session_id"] + ".plk", "wb") as f:
    pickle.dump(chat_history, f)
print("ずんだもん：会話内容を保存したのだ．また今度なのだ．")
s.close()

