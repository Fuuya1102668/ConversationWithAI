import re

import torch
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain, LLMChain
from langchain.prompts import PromptTemplate
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

prompt = ChatPromptTemplate.from_messages(
        [
            (
               "system",
"""
"[INST]僕はずんだもんです．僕はずんだの妖精です．僕はJTCで働いており，pythonのエンジニアです．
humanが問いかけますので，placeholderを参考にもっともらしい返答を生成してください．[/INST]
"""),
            ("placeholder", "{chat_history}"),
            ("human", "{user_input}"),
        ]
)

memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = memory | prompt | llm

while True:
    user_input = input("フウヤ：")
    response = llm_chain.invoke({"user_input":user_input})
    response = extract_text_after_inst(response)
    print("ずんだもん：" + response)
#    print(type(response))

