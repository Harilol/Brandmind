import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")
# print(f"Key loaded: {api_key[:10]}..." if api_key else "NO KEY FOUND")

# client = genai.Client(api_key=api_key)

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents="Say exactly: SETUP WORKS"
# )

# print("Response:", response.text)


import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize the model (automatically reads GROQ_API_KEY)
# Popular models include: llama-3.3-70b-versatile, llama-3.1-8b-instant, gemma2-9b-it
model = ChatGroq(
    model="openai/gpt-oss-safeguard-20b",
    temperature=0,
)

messages = [
    SystemMessage(content="You are a helpful culinary assistant."),
    HumanMessage(content="Give me a quick recipe for scrambled eggs."),
]

response = model.invoke(messages)
print(response.content)
