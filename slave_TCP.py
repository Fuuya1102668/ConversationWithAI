import getapi as get
import socket
import pickle
import io
import simpleaudio as sa
import sounddevice as sd
from scipy.io.wavfile import write
import keyboard
import numpy as np
import cv2
import time
from multiprocessing import Process

#########
# SLAVE #
#  TCP  #
#########

# 録音設定
sample_rate = 44100  # サンプリング周波数
channels = 2  # ステレオ録音

# 録音データを格納するリスト
recorded_frames = []

# 動画再生のインスタンス生成
video1 = "kutipaku.mp4"
video2 = "dottimo.mp4"

cap1 = cv2.VideoCapture(video1)
cap2 = cv2.VideoCapture(video2)

# ウィンドウの名前を指定
window_name = 'Video Player'

# フレームレートを設定
fps = 30
delay = int(1000 / fps)

def display_video(cap, window_name):
    while True:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow(window_name, frame)
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                return

# ウィンドウを作成し、動画を交互に表示するループ
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

master_ip = get.get_master_ip()
master_port = int(get.get_master_port())
slave_port = int(get.get_slave_port())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((master_ip, master_port))

# プロセスの作成
process1 = Process(target=display_video, args=(cap1, window_name))

# プロセスの開始
process1.start()

print("Connected to server")

try:
    while True:
        inputs = input("  あなた  ：")
        s.sendall(inputs.encode())

        if inputs.lower() == "exit":
            break
        
        response = b''
        while True:
            part = s.recv(4096)
            if b'__end__' in part:
                print("Data received")
                print("Total : ", len(response))
                response += part.replace(b'__end__', b'')
                break
            response += part
            print("response :", len(response))

        
        response_content = pickle.loads(response)
        print("Response played")
        sa.WaveObject.from_wave_file(io.BytesIO(response_content)).play().wait_done()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    process1.join()
    #process2.join()
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()
    s.close()
    print("Connection closed")

