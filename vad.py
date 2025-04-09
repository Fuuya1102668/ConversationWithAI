import numpy as np
import webrtcvad
import sounddevice as sd
import wave
import time
from faster_whisper import WhisperModel
import threading

class VoiceActivityDetector:
    def __init__(self, rate=16000, chunk=320, channels=1, vad_mode=3, min_speech_duration=0.5, silence_threshold=1.0):
        self.RATE = rate
        self.CHUNK = chunk
        self.CHANNELS = channels
        self.VAD_MODE = vad_mode
        self.MIN_SPEECH_DURATION = min_speech_duration
        self.SILENCE_THRESHOLD = silence_threshold
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(self.VAD_MODE)
        self.model = WhisperModel("large-v2", device="cuda", compute_type="float16")
        # self.model = WhisperModel("large-v2", device="cpu", compute_type="int8")
        self.recording = []
        self.recording_active = False
        self.silent_duration = 0
        self.speech_duration = 0
        self.filename = "recorded_audio.wav"
        self.transcribed_text = ""

    def is_human_voice(self, audio_data):
        volume = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
        return np.mean(np.abs(volume)) > 500  # 閾値を調整

    def save_audio_and_transcribe(self):
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.recording))
        print(f"Saved: {self.filename}")
        results, info = self.model.transcribe(self.filename, language="ja")
        for result in results:
            self.transcribed_text += result.text
        print("Recognized Text:", self.transcribed_text)
        self.recording = []

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        audio_data = indata[:, 0].astype(np.int16).tobytes()
        is_speech = self.vad.is_speech(audio_data, self.RATE) and self.is_human_voice(audio_data)
        
        if is_speech:
            if not self.recording_active:
                self.recording_active = True
                self.speech_duration = 0  # 発話の継続時間をリセット
                self.silent_duration = 0  # 無音時間をリセット
            self.speech_duration += self.CHUNK / self.RATE
            self.recording.append(audio_data)
        else:
            if self.recording_active:
                self.silent_duration += self.CHUNK / self.RATE
                if self.silent_duration < self.SILENCE_THRESHOLD:
                    return
                if self.speech_duration >= self.MIN_SPEECH_DURATION:
                    self.recording_active = False
                    self.silent_duration = 0
                    threading.Thread(target=self.save_audio_and_transcribe).start()
                else:
                    self.recording = []
                    self.recording_active = False
                    self.silent_duration = 0
                    print("Recording discarded due to short speech duration.")

    def listen_and_transcribe(self):
        with sd.InputStream(samplerate=self.RATE, channels=self.CHANNELS, blocksize=self.CHUNK, dtype='int16', callback=self.callback):
            print("Listening...")
            while True:
                time.sleep(0.1)
                if self.transcribed_text:
                    return self.transcribed_text
