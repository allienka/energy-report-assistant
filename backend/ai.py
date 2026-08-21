import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(findings):
    response = client.responses.create(
    model="gpt-5.6",
    input=f"""
            You are an energy analyst.

            Analyze these findings:
            {findings}

            Write a short professional summary.
            """
)
    return response.output_text     


