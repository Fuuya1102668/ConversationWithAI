from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import voice
import sounddevice as sd

model_id = "models/marged_model/"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

messages = [
    {"role": "system", "content": "あなたはずんだもんです．日本の伝統的な企業で働いているpythonのエンジニアです．"},
    {"role": "user", "content": "自己紹介してください．"},
    {"role": "system", "content": "僕の名前はずんだもんなのだ！"},
    {"role": "user", "content": "私の名前はフウヤです．これからよろしくね！"},
    {"role": "system", "content": "フウヤさん，よろしくお願いします．"},
    {"role": "user", "content": "これからも楽しくお話していきましょう．"},
]

input_ids = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device)

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

while True:
    outputs = model.generate(
        input_ids,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )

    response = outputs[0][input_ids.shape[-1]:]
    outputs = tokenizer.decode(response, skip_special_tokens=True)
    print("ずんだもん：" + outputs)
    print(messages)
    inputs = input("あなた：")
    #sr, audio = voice.generate(outputs)
    #sd.play(audio, sr)
    #sd.wait()
    #inputs = input("あなた：")
    #messages.append({"role": "system", "content": outputs})
    #messages.append({"role": "user", "content": inputs})

