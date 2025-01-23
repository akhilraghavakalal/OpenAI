import os
from dotenv import load_dotenv  # for loading the API key from the .env file
import openai  # to use openAI

load_dotenv()  # loads the environment variables

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)  # loading the key from the loaded env variables

# creating the client and configuring the key
client = openai.OpenAI(api_key=OPENAI_API_KEY)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[ # messages is a list of dictionaires [{role, content},{role, content}, ..]
        {
            "role": "user",
            # user (similar to how type in chatGPT),
            # developer (sets the main context of chat, higher priority than the user role,
            # assistant (responses from the openai model ex: Knock Knock jokes) )
            "content": "trying the API connection for the first time. Hope it works !!",
        }
    ],
)

# print(response)
print(response.choices[0].message.content)
