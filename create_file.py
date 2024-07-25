import openai
import getapi

api = getapi.get_api()
openai.api_key = api

openai.files.create(
    file=open("./zmn.jsonl", "rb"),
    purpose="fine-tune"
    )

