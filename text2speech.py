import getapi
import os
import requests

ip = getapi.get_master_ip()

def generate_speech(text):
    url = "http://" + ip + ":5000/voice"
    #url = "http://192.168.11.45:4649/voice"
    headers = {"accept":"audio/wav"}
    params = {
        "text":text,
        "encodeng":"utf-8",
        "model_name":"zundamon",
    }
    
    return requests.post(url, headers=headers, params=params)

if __name__ == "__main__":
    from pydub import AudioSegment
    from pydub.playback import play
    import io

    print("IP ADDRESS : ", ip)
    while True:
        text = input("音声にしたいテキスト：")
        response = generate_speech(text)
        audio_segment = AudioSegment.from_file(io.BytesIO(response.content), format="wav")
        play(audio_segment)

