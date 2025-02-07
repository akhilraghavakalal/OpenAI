from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# creating the client
client = OpenAI(api_key=OPENAI_API_KEY)

# 1. Creating a Vector Store
vector_store = client.beta.vector_stores.create(name="KnowledgeBase")

# 2. Prepare the files to upload to the vector store
file_paths = [
    "./files/a.txt",
    "./files/b.txt",
    "./files/Lab2.pdf",
]
file_streams = [open(path, "rb") for path in file_paths]

# 3. Uploading the files to vector store
# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)

print(file_batch.status)
print(file_batch.file_counts)

# 4. Creating an assistant
assistant = client.beta.assistants.create(
    name="Genieee",
    model="gpt-4o",
    tools=[
        {"type": "code_interpreter"},
        {"type": "file_search"},
    ],
    # strict instructions to limit the assistant to answer only from the content of files not outside it
    instructions="""You are an assistant that MUST ONLY answer questions based on the content of the attached files.
    If the answer cannot be found in the attached files, respond with: 'I cannot answer this question as the information is not present in the provided files.'
    You can use the code interpreter to perform calculations, create visualizations, or analyze data when requested.
    Do not use any external knowledge or make assumptions beyond what is explicitly stated in the files.
    Always base your responses solely on the content found in the attached documents.""",
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)


# Now that the assistant is created and file is uploaded go to the next step
# 5. Creating a thread and attaching the uploaded file to thread
thread = client.beta.threads.create()

# once we have everything ready, just run the assistant
# 6. Run the assistant & thread, but in the form of a 2 way chat
print("\nEnter an query, enter quit to exit")
while True:
    print("\nQuery: ", end="")
    user_query = input()
    if user_query.lower() == "quit":
        break

    # Add the user query to the exisiting thread, file is already attached
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_query
    )

    # run the query inside the thread using create and poll
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )
    # print("Run Status is: ", run.status)

    # get the latest response from the thread
    response = client.beta.threads.messages.list(thread_id=thread.id)
    # print(response)
    latest_response = response.data[0].content[0].text.value.split("【")[0].strip()
    print("\nResponse: ", end="")
    print(latest_response)
