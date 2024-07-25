import openai
import getapi

api = getapi.get_api()
openai.api_key = api

openai.files.create(
    file=open("./zmn.jsonl", "rd"),
    purpose="fine-tune"
    )

