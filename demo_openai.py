import argparse
from openai import OpenAI

import sys
from io import StringIO
import base64
import requests
from together import Together
from dotenv import load_dotenv
import os
from contextlib import redirect_stdout
from demo_perplexity import extract_code_blocks

# Load environment variables from .env file
load_dotenv()

# def together_model(file_path, language, country, api_key=None, model="Llama-3.2-90B-Vision"):
#     # Get the API key from environment if not provided
#     if api_key is None:
#         api_key = os.getenv("TOGETHER_API_KEY")
    
#     vision_llm = "meta-llama/Llama-Vision-Free" if model == "free" else f"meta-llama/{model}-Instruct-Turbo"
#     client = Together(api_key=api_key)
#     final_markdown = get_json(client, vision_llm, file_path, language, country)
#     return final_markdown
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def test(prompt):
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=2048,
    temperature=0.9,
    )
    print(completion.choices[0].message)

def llm(prompt):
    # Load the system prompt from prompt.txt
    with open('prompt.txt', 'r') as file:
        sys_prompt = file.read()
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10240,
        temperature=0.9,
    )
    message = completion.choices[0].message
    try:
        if 'Complete Code' in message.content:
            script = message.content.split('Complete Code')[1].split('```python')[1].split('```')[0]
        else:
            script = extract_code_blocks(message.content)
            script = ('\n').join(script)
            # explain = splits[0]
    except:
        script = []
    explain = message.content
    # f = open("script.py", "w")
    # f.write(script)
    # f.close()
    # print(citations)
    output=''
    if script:
        redirected_output = StringIO()
        with redirect_stdout(redirected_output):
            exec(script)
        output = redirected_output.getvalue()
    output = output+'\n'+explain
    
    return script, [], output

    
def main():
    parser = argparse.ArgumentParser(description='Process a prompt for the LLM.')
    parser.add_argument('prompt', type=str, help='The prompt to send to the LLM')
    args = parser.parse_args()

    # Call the llm function with the provided prompt
    response = llm(args.prompt)
    print(response)

if __name__ == "__main__":
    # test("Hi!")
    
    question = 'List all food items in the dataset that contain traces of "CARTA."'
    llm(question)
    
    # question = 'Which vegetable in the dataset has the highest amount of vitamin C per 100 grams?'
    # llm(question)

    # main()