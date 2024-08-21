import getapi as get
import socket
import pickle
import io
import simpleaudio as sa
import sounddevice as sd
from scipy.io.wavfile import write
import keyboard
import numpy as np

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
player = mpv.MPV(volume=0, loop="inf", fullscreen=True)

def start_recording():
    global recording
    print("Recording started...")
    recording = True
    while recording:
        frame = sd.rec(1024, samplerate=sample_rate, channels=channels, dtype='float64')
        sd.wait()
        recorded_frames.append(frame)

def stop_recording():
    global recording
    recording = False
    print("Recording stopped.")
    # リストに格納した録音データを1つの配列に結合
    recorded_data = np.concatenate(recorded_frames, axis=0)
    write("input.wav", sample_rate, recorded_data)

master_ip = get.get_master_ip()
master_port = int(get.get_master_port())
slave_port = int(get.get_slave_port())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((master_ip, master_port))

print("Connected to server")

try:
    recording = False
    print("Press the Space key to start/stop recording.")
    while True:
        if keyboard.is_pressed('space'):
            if not recording:
                recorded_frames = []  # 録音データのリストをリセット
                start_recording()
            else:
                stop_recording()
        s.sendall(input.wav)
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
        player.pause = True
        sa.WaveObject.from_wave_file(io.BytesIO(response_content)).play()
        print("Response played")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    s.close()
    print("Connection closed")

