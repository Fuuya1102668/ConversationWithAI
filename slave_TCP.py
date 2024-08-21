import getapi as get
import socket
import pickle
import io
import simpleaudio as sa
import sounddevice as sd
from scipy.io.wavfile import write
import keyboard
import numpy as np
import mpv

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
video01 = "kutipaku.mp4"
video02 = "dottimo.mp4"
#player01 = mpv.MPV(volume=0, loop="inf", fullscreen=True)
#player02 = mpv.MPV(volume=45, loop="inf", fullscreen=True)
player01 = mpv.MPV(volume=0, loop="inf", ontop=True)
player02 = mpv.MPV(volume=45, loop="inf", ontop=False)
player01.play(video01)
player02.play(video02)

master_ip = get.get_master_ip()
master_port = int(get.get_master_port())
slave_port = int(get.get_slave_port())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((master_ip, master_port))

print("Connected to server")

try:
    while True:
        player01.stop()
#        player01.ontop = False
        player02.pause = False
#        player02.ontop = True
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
        player02.pause = True
        player01.play(video01)
        sa.WaveObject.from_wave_file(io.BytesIO(response_content)).play().wait_done()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    s.close()
    print("Connection closed")

