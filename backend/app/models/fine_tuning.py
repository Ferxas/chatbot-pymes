from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


client.files.create(
  file=open("train.jsonl", "rb"),
  purpose="fine-tune"
)

print(client)