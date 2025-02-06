from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# creating the client
client = OpenAI(api_key=OPENAI_API_KEY)

# 1. Creating an assistant
assistant = client.beta.assistants.create(
    name="Genieee",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
    instructions="You are a genie that can answer questions to the user based on your knowledge base only.",
)

# 2. Upload a single file to the assistant
knowledge_file = client.files.create(
    file=open("./files/a.txt", "rb"), purpose="assistants"
)

print("Knowledge File is : ", knowledge_file)

# Now that the assistant is created and file is uploaded go to the next step
# 3. Creating a thread and attaching the uploaded file to thread
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "What is the name of the main character ? also what is the full name",
            "attachments": [
                {"file_id": knowledge_file.id, "tools": [{"type": "file_search"}]}
            ],
        }
    ]
)

print("My print message is")
print(thread.tool_resources.file_search)

# once we have everything ready, just run the assistant
# 4. Run the assistant & thread
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)
print(run.status)
# get all the messages of the thread
messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

# display the content
message_content = messages[0].content[0].text.value

print(message_content)

print(messages)

