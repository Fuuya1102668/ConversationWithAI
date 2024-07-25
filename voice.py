from style_bert_vits2.nlp import bert_models
from style_bert_vits2.constants import Languages
from pathlib import Path
from style_bert_vits2.tts_model import TTSModel
import sounddevice as sd


def load_model(model_file,config_file,style_file):
    bert_models.load_model(Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")
    bert_models.load_tokenizer(Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")

    #モデルインスタンスの作成
    model = TTSModel(
        model_path=model_file,
        config_path=config_file,
        style_vec_path=style_file,
        device="cuda",
    )

    return model
    
if __name__ == "__main__":
    #モデルの重みが格納されているpath
    assets_root = Path("../Style-Bert-VITS2/model_assets/zundamon/")
    model_file = assets_root / "zundamon_e100_s16200.safetensors"
    config_file = assets_root / "config.json"
    style_file = assets_root / "style_vectors.npy"
    
    model = load_model(model_file=model_file, config_file=config_file, style_file=style_file)
    while True:
        text = input("入力：")
        sr, audio = model.infer(text=text)
        #再生
#        sd.play(audio, sr)
#        sd.wait()

