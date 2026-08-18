import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai():
    response = client.responses.create(
    model="gpt-5.6",
    input="""
            You are an energy analyst.
            Explain what COP means and why a significant decrease in COP could be important.
            Keep the answer to 2 sentences.
            """
)
    return response.output_text     
print(ask_ai())