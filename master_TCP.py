import character_langchain02_RAG_PDF as rag
import text2speech as t2s
import getapi as get
import pickle
import os

import socket

os.environ["OPENAI_API_KEY"] = get.get_api()
slave_ip = get.get_slave_ip()
slave_port = int(get.get_slave_port())
master_port = int(get.get_master_port())

# ソケットの設定と接続の待機
def setup_server_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", port))
    s.listen(1)
    print("Server is listening on port", port)
    return s

s = setup_server_socket(master_port)

config = {"configurable": {"session_id": "zunda"}}
#model_name = "ft:gpt-3.5-turbo-0125:personal::9ol99gYa"
model_name = "gpt-4o-mini"
directory = "./rag_source"
file = "*.pdf"
contextualize_q_system_prompt = (
    "チャット履歴と，チャット履歴のコンテキストを参照する可能性のある最新のユーザの質問が与えられた場合，チャット履歴を優先的に参照して質問に答えてください．"
)
qa_system_prompt = "あなたの名前は「ずんだもん」です．語尾は「なのだ」です．金沢工業大学で学生をしています．たかごう先生の研究室に所属し，UNIXについて研究しています．回答は必ず，contextとhistoryを参照してから行ってください．{context}"

text_model = rag.create_chat_model(model_name)
retriever = rag.loade_pdf(directory, file)
conversational_rag_chain = rag.create_chain(text_model, retriever, contextualize_q_system_prompt, qa_system_prompt)

try:
    with open("history_" + config["configurable"]["session_id"] + ".plk", "rb") as f:
        chat_history = pickle.load(f)
except FileNotFoundError:
    chat_history = []

print("System startup is complete.")

def handle_client_connection(conn):
    global chat_history
    while True:
        try:
            print("waiting...")
            inputs = conn.recv(4096)
            if not inputs:
                break
            print("data received")
            inputs = inputs.decode()
            print("inputs : " + str(inputs))
            if inputs.lower() == "exit":
                break

            # ストリーム開始
            stream = conversational_rag_chain.stream(
                {"input": inputs},
                config=config,
            )

            # ストリーミング出力の分割と音声変換
            buffer = ""
            for chunk in stream:
                content = chunk.get("answer", "")
                buffer += content
                print(content, end="", flush=True)

                while any(p in buffer for p in "。、！"):
                    for i, char in enumerate(buffer):
                        if char in "。、！":
                            segment = buffer[:i+1]
                            buffer = buffer[i+1:]
                            print(f"\n[音声送信] {segment}")
                            response = t2s.generate_speech(segment)
                            response = pickle.dumps(response.content)
                            conn.sendall(response)
                            conn.sendall(b'__end__')
                            break

            # 最後の残りも送信
            if buffer.strip():
                print(f"\n[残り音声送信] {buffer}")
                response = t2s.generate_speech(buffer)
                response = pickle.dumps(response.content)
                conn.sendall(response)
                conn.sendall(b'__end__')

            # 履歴追加
            chat_history = rag.add_history(chat_history, inputs, {"answer": buffer})
            print("done")
        except (BrokenPipeError, ConnectionResetError, socket.timeout) as e:
            print(f"Error: {e}, connection lost")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

    with open("history_" + config["configurable"]["session_id"] + ".plk", "wb") as f:
        pickle.dump(chat_history, f)
    print("ずんだもん：会話内容を保存したのだ．また今度なのだ．")

while True:
    try:
        conn, addr = s.accept()
        print("Connection from", addr)
        handle_client_connection(conn)
        conn.close()
    except KeyboardInterrupt:
        print("Server is shutting down.")
        break
    except Exception as e:
        print(f"Error accepting connections: {e}")

s.close()

