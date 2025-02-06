from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# creating the client
client = OpenAI(api_key=OPENAI_API_KEY)

# 1. Create a Vector Store
vector_store = client.beta.vector_stores.create(name="KnowledgeBase")

# Ready the files for upload to OpenAI
file_paths = ["./files/a.txt"]
file_streams = [open(path, "rb") for path in file_paths]

# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)

print(file_batch.status)
print(file_batch.file_counts)