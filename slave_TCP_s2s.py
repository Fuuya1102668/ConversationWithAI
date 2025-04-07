import getapi as get
import vad
import socket
import pickle
import io
import tempfile
import os
import subprocess
import threading

#########
# SLAVE #
#  TCP  #
#########

current_proc_lock = threading.Lock()
current_proc = None

def play_audio_async(audio_bytes):
    global current_proc

    # 再生中プロセスがあれば停止
    with current_proc_lock:
        if current_proc and current_proc.poll() is None:
            current_proc.terminate()

        # 新しい再生を開始（非同期）
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        proc = subprocess.Popen([
            "ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", tmp_path
        ])
        current_proc = proc

def stop_audio_playback():
    global current_proc
    with current_proc_lock:
        if current_proc and current_proc.poll() is None:
            current_proc.terminate()
        current_proc = None

# 接続設定
master_ip = get.get_master_ip()
master_port = int(get.get_master_port())
slave_port = int(get.get_slave_port())

cv_ip = "127.0.0.1"
cv_port = 23456

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((master_ip, master_port))

cv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Connected to server")

try:
    while True:
        # 映像切替指示（入力開始）
        cv_sock.sendto(b"video1", (cv_ip, cv_port))

        # 音声入力（非同期再生中でも即開始）
        VAD = vad.VoiceActivityDetector()
        inputs = VAD.listen_and_transcribe()
        print(f"  あなた  ：{inputs}")
        s.sendall(inputs.encode())

        if inputs.lower() == "exit":
            break

        # レスポンスの受信
        response = b''
        while True:
            part = s.recv(4096)
            if b'__end__' in part:
                print("Data received")
                print("Total Data :", len(response))
                response += part.replace(b'__end__', b'')
                break
            response += part

        try:
            response_content = pickle.loads(response)
            print("Response received")

            # 映像切替（応答再生）
            cv_sock.sendto(b"video2", (cv_ip, cv_port))

            # 再生中の音声を止めて，新しい音声を非同期再生
            play_audio_async(response_content)

        except Exception as e:
            print(f"音声処理エラー: {e}")

except Exception as e:
    print(f"システムエラー: {e}")

finally:
    s.close()
    cv_sock.close()
    stop_audio_playback()
    print("Connection closed")
