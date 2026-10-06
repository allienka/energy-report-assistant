import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(findings):
    response = client.responses.create(
        model="gpt-5.6",
        input=f"""
You are an energy analyst reviewing monthly energy data.

Analyze the following detected findings:

{json.dumps(findings, indent=2)}

Write a short professional report summary.

For each significant finding:
- Mention the affected device.
- Describe what changed.
- Include the numerical change.
- Explain why the change may be relevant.
- Do not invent causes or information that is not provided.

If there are multiple findings, prioritize the most significant ones.

Keep the report concise and suitable for a professional energy monitoring report.
"""
    )

    return response.output_text  


