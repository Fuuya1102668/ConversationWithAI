import socket
import pyaudio
import getapi as get

master_port = int(get.get_master_port())

# PyAudioの設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# PyAudioオブジェクトの作成
audio = pyaudio.PyAudio()

# 再生ストリームを作成
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, output=True,
                    frames_per_buffer=CHUNK)

# サーバーソケットの設定
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", master_port))
s.listen(1)
print("Server is listening on port", master_port)

def receive_and_play(conn):
    try:
        audio_data = b''
        while True:
            part = conn.recv(4096)
            if b'__end__' in part:
                audio_data += part.replace(b'__end__', b'')
                break
            audio_data += part

        if audio_data:
            print("Audio data received")
            stream.write(audio_data)
            print("Audio data played")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()

while True:
    try:
        conn, addr = s.accept()
        print("Connection from", addr)
        receive_and_play(conn)
    except KeyboardInterrupt:
        print("Server is shutting down.")
        break
    except Exception as e:
        print(f"Error accepting connections: {e}")

s.close()
stream.stop_stream()
stream.close()
audio.terminate()
print("Server closed")

