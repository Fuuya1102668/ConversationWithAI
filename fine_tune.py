import openai
import getapi

api = getapi.get_api()
openai.api_key = api

print("create fine-tune file")

file = openai.files.create(
    file=open("./zmn.jsonl", "rb"),
    purpose="fine-tune",
    )

print("file id :" + file.id)
print("start fine-tune")

job = openai.fine_tuning.jobs.create(
    model="gpt-4o-mini-2024-07-18",
    training_file=file.id,
    )

print("job id :" + job.id)

res = openai.fine_tuning.jobs.retrieve(job.id)

if res.error.code is not None:
    print("Error Code :", res.error.code)
    print("Error Message :", res.error.message)
else:
    print("Status :", res.status)
    print("Fine Tuned Model ID :", res.fine_tuned_model)


