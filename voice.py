from style_bert_vits2.nlp import bert_models
from style_bert_vits2.constants import Languages
from pathlib import Path
from style_bert_vits2.tts_model import TTSModel
import sounddevice as sd

def generate(text):
    bert_models.load_model(Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")
    bert_models.load_tokenizer(Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")

#モデルの重みが格納されているpath
    model_file = "zundamon/zundamon_e100_s16200.safetensors"
    config_file = "zundamon/config.json"
    style_file = "zundamon/style_vectors.npy"

    assets_root = Path("../Style-Bert-VITS2/model_assets")

#モデルインスタンスの作成
    model = TTSModel(
        model_path=assets_root / model_file,
        config_path=assets_root / config_file,
        style_vec_path=assets_root / style_file,
        device="cuda",
    )

    # 音声を生成する
    sr, audio = model.infer(text=text)

    return sr, audio

if __name__ == "__main__":
    while True:
        text = input("入力：")
        sr, audio = generate(text)
        #再生
        sd.play(audio, sr)
        sd.wait()

