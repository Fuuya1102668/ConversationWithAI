import threading
import queue
import getapi as get
import vad
import socket
import pickle
import io
import sounddevice as sd
import soundfile as sf

# サーバ設定
master_ip = get.get_master_ip()
master_port = int(get.get_master_port())

# TCPソケット
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((master_ip, master_port))

# UDPソケット（映像制御用）
cv_ip = "127.0.0.1"
cv_port = 23456
cv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Connected to server")

# 音声応答データの受信キュー
playback_queue = queue.Queue()

# TCP受信スレッド
def tcp_receiver():
    try:
        while True:
            response = b''
            while True:
                part = s.recv(4096)
                if b'__end__' in part:
                    response += part.replace(b'__end__', b'')
                    break
                response += part
            response_content = pickle.loads(response)
            playback_queue.put(response_content)
    except Exception as e:
        print(f"[Receiver] Error: {e}")

def playback_worker():
    while True:
        wav_bytes = playback_queue.get()  # キューから取得（ブロッキング）
        try:
            with sf.SoundFile(io.BytesIO(wav_bytes), 'rb') as f:
                data = f.read(dtype='float32')
                sd.play(data, f.samplerate)
                sd.wait()  # 再生完了を待つ（このスレッド内で完結）
        except Exception as e:
            print(f"[Playback] Error: {e}")
        playback_queue.task_done()

def stop_all_playback():
    # 再生中の音声を停止
    sd.stop()
    
    # キューを空にする（1つずつ取り出して捨てる）
    while not playback_queue.empty():
        try:
            playback_queue.get_nowait()
            playback_queue.task_done()
        except queue.Empty:
            break

    print("[Playback] All playback stopped and queue cleared.")

# 受信スレッド開始
threading.Thread(target=tcp_receiver, daemon=True).start()
threading.Thread(target=playback_worker, daemon=True).start()

try:
    while True:
        # 音声認識 → 送信
        cv_sock.sendto(b"video1", (cv_ip, cv_port))
        VAD = vad.VoiceActivityDetector()
        inputs = VAD.listen_and_transcribe()
        print(f"  あなた  ：{inputs}")
        s.sendall(inputs.encode())
        stop_all_playback()

        if inputs.lower() == "exit":
            break

        # 受信待ち（非同期的に受信される）
        print("Waiting for response...")
        response = playback_queue.get()  # ブロッキングで待機

        print("Response played")
        cv_sock.sendto(b"video2", (cv_ip, cv_port))

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    s.close()
    cv_sock.close()
    print("Connection closed")
