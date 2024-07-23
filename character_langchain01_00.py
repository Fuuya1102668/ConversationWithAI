import re

import torch
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain, LLMChain
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
#from langchain.memory.buffer import ConversationBufferMemory

def extract_text_after_inst(input_text):
    # Define the regex pattern to find text after [/INST]
    pattern = r'\[/INST\](.*)'
    match = re.search(pattern, input_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"\n!!! current device is {device} !!!\n")

quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_btype=torch.bfloat16
        )

model_path = "./models/marged_model/"
tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=model_path,
        )
model = AutoModelForCausalLM.from_pretrained(
        quantization_config=quantization_config,
        pretrained_model_name_or_path=model_path,
        device_map={"": "cuda:0"}
        )

task = "text-generation"
pipe = pipeline(
    task, 
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=128,
)

llm = HuggingFacePipeline(pipeline=pipe)

template = """
"[INST]あなたは人間と話すチャットボットです．名前を「ずんだもん」といい，ずんだの妖精です．ずんだもんはJTCで働いており，pythonのエンジニアです．
[/INST]

user:こんにちは！
ずんだもん：こんにちはなのだ！

user:私の名前はフウヤです．よろしくおねがいします．
ずんだもん:フウヤさん！僕の名前はずんだもんなのだ！よろしくお願いするのだ．

{chat_history}

user:{user_input}
ずんだもん:
""" 

prompt = PromptTemplate(
    input_variables=["chat_history", "user_input"],
    template=template
    )

memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
) 

while True:
    user_input = input("フウヤ：")
    response = llm_chain.predict(user_input=user_input)
    print("ずんだもん：" + response)
#    print(type(response))

