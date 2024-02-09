from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "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"))
completion = client.chat.completions.create(
   model="ft:gpt-3.5-turbo-0613:dathway::8qFUMuKc",
   messages=[
     {"role": "system", "content": "You are a tech career assistant. You chat with users and you ask them 5 questions about their socio-activities and academic background to help them decipher what tech skill they should learn. At the end suggest 5 tech skills and rate them according to their compatibility with the person over 10."},
     {"role": "user", "content": "1. drawing 2. with a team "}
   ]
 )

print(completion.choices[0].message)


