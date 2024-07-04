import torch
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain.chains import ConversationChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig

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
    max_new_tokens=32,
)

llm = HuggingFacePipeline(pipeline=pipe)

prompt = PromptTemplate(
        template="""
"[INST]あなたはずんだもんです．ずんだもんはずんだの妖精です．ずんだもんはJTCで働いており，pythonのエンジニアです．一人称は僕です．会話相手の名前はフウヤです．
フウヤ: {user_input}
ずんだもん：[/INST]
""",
        input_variables=["user_input"]
        )

llm_chain = prompt | llm

while True:
    user_input = input("フウヤ：")
    response = llm_chain.invoke({"user_input":user_input})
    print(response)
#    print(type(response))

