# this is to test if the API to be working
from openai import OpenAI

client = OpenAI(api_key="")
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a song about srilanka."},
    ],
)


print(completion.choices[0].message.content)
