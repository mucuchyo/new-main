import os
import openai

openai.api_key = "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"

prompt = input("지시사항을 입력하세요 : ")

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0.5,
  max_tokens=300,

)
print("=======================================")
print(response["choices"][0]["text"].strip())
print("=======================================")


