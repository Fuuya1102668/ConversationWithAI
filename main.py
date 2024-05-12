import ollama
import requests
import json
import subprocess
import time
import os
import sounddevice as sd
import numpy as np

def start_voicevox():
    voicevox_path = "../.voicevox/VOICEVOX.AppImage"  # Voicevoxのパスを適宜変更してください
    voicevox_process = subprocess.Popen(
        [voicevox_path],
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(10)  # Voicevoxの起動待ち時間（秒）

def stop_voicevox():
    subprocess.run(["pkill", "-f", "VOICEVOX.AppImage"])

def chat_with_ollama(messages):
    response = ollama.chat(
        model="znd",
        messages=messages,
    )
    return response["message"]["content"]

def generate_voice(text):
    url = "http://localhost:50021/audio_query"
    params = (
        ("text", text),
        ("speaker", 3),  # ずんだもんの話者番号
    )
    response = requests.post(url, params=params)
    query = response.json()

    url = "http://localhost:50021/synthesis"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(query), headers=headers, params=params)

    voice = response.content
    samples = np.frombuffer(voice, dtype=np.int16)
    sd.play(samples, samplerate=24000, blocking=True)


def main():
    start_voicevox()  # Voicevoxを起動

    print("Welcome to the Ollama chatbot!")
    print("Type 'quit' or press 'Ctrl+D' to exit the conversation.")

    messages = []
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print("Thank you for chatting with Ollama. Goodbye!")
                break

            messages.append({"role": "user", "content": user_input})
            response_text = chat_with_ollama(messages)
            messages.append({"role": "assistant", "content": response_text})
            print(f"Ollama: {response_text}")

            generate_voice(response_text)

        except EOFError:
            print("\nThank you for chatting with Ollama. Goodbye!")
            break

    stop_voicevox()  # Voicevoxを終了

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nThank you for chatting with Ollama. Goodbye!")
        stop_voicevox()  # Voicevoxを終了