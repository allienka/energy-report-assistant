import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(findings):
    response = client.responses.create(
    model="gpt-5.6",
    input="""
            You are an energy analyst.

            Analyze these findings:
            {findings}

            Write a short professional summary.
            """
)
    return response.output_text     


test_findings = [
    {
        "type": "cop_drop",
        "device": "Pump A",
        "value": -1.2
    },
    {
        "type": "alarm_increase",
        "device": "Pump C",
        "value": 6
    }
]
print(ask_ai(test_findings))