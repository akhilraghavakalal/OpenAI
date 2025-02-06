import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# creating the client
client = OpenAI(api_key=OPENAI_API_KEY)

# user message
user_queries = []

while True:
    print("Enter the query: ")
    user_message = input()
    if user_message.lower() == "quit":
        break
    else:
        user_queries.append({"role": "user", "content": user_message})
        response = client.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=user_queries,
            max_tokens=100,  # setting up this max tokens to handle the cost utilization
        )

        llm_response = response.choices[0].message.content
        print("\nResponse: \n", llm_response, "\n")
        user_queries.append({"role": "assistant", "content": llm_response})

print("\nChat details: \n",user_queries)
