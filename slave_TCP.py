import getapi as get
import socket
import pickle
import io
import simpleaudio as sa
import sounddevice as sd
from scipy.io.wavfile import write
import keyboard
import numpy as np
import time

#########
# SLAVE #
#  TCP  #
#########

# 録音設定
sample_rate = 44100  # サンプリング周波数
channels = 2  # ステレオ録音

# 録音データを格納するリスト
recorded_frames = []

master_ip = get.get_master_ip()
master_port = int(get.get_master_port())
slave_port = int(get.get_slave_port())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((master_ip, master_port))

cv_ip = "127.0.0.1"
cv_port = 23456

cv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Connected to server")

try:
    while True:
        cv_sock.sendto(b"video1", (cv_ip, cv_port))
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
        cv_sock.sendto(b"video2", (cv_ip, cv_port))
        sa.WaveObject.from_wave_file(io.BytesIO(response_content)).play().wait_done()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    s.close()
    cv_sock.close()
    print("Connection closed")

