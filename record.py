import sounddevice as sd
from scipy.io.wavfile import write
from pynput import keyboard
import numpy as np

# 録音設定
sample_rate = 44100  # サンプリング周波数
channels = 2  # ステレオ録音

# 録音データを格納するリスト
recorded_frames = []
recording = False

def on_press(key):
    global recording, recorded_frames

    if key == keyboard.Key.space:
        if not recording:
            print("Recording started...")
            recording = True
        else:
            print("Recording stopped.")
            recording = False

            # 録音データを結合して保存
            recorded_data = np.concatenate(recorded_frames, axis=0)
            write("output.wav", sample_rate, recorded_data)
            print("Saved as output.wav")

            # 録音データのリストをクリア
            recorded_frames = []

def on_release(key):
    if key == keyboard.Key.esc:
        # Escキーが押されたらプログラムを終了
        return False

def record_audio():
    global recording
    with sd.InputStream(samplerate=sample_rate, channels=channels, dtype='float32') as stream:
        while True:
            if recording:
                frame = stream.read(1024)[0]
                recorded_frames.append(frame)

if __name__ == "__main__":
    print("Press the Space key to start/stop recording.")
    print("Press Esc to exit.")

    # リスナーを別スレッドで起動
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # 録音スレッドを開始
    record_audio()

    # リスナーの終了を待機
    listener.join()

