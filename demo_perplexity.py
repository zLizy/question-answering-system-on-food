import argparse
from openai import OpenAI

from io import StringIO
from dotenv import load_dotenv
import os
from contextlib import redirect_stdout

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

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")



def test(prompt=''):
    messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant and you need to "
            "engage in a helpful, detailed, polite conversation with a user."
        ),
    },
    {   
        "role": "user",
        "content": (
            "How many stars are in the universe?"
        ),
    },
]
    
    # chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3.1-sonar-large-128k-online",
        messages=messages,
    )
    print(response)

def llm(prompt):
    # Load the system prompt from prompt.txt
    with open('prompt.txt', 'r') as file:
        sys_prompt = file.read()
    
    completion = client.chat.completions.create(
        model="llama-3.1-sonar-large-128k-online",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    message = completion.choices[0].message
    
    try:
        citations = completion.citations
    except AttributeError:
        citations = []
    try:
        if 'Complete Code' in message.content:
            script = message.content.split('Complete Code')[1].split('```python')[1].split('```')[0]
        elif 'combined code' in message.content.lower():
            script = message.content.split('combined code')[1].split('```python')[1].split('```')[0]
        else:
            script = message.content.split('```python')[-1].split('```')[0]
            # script = extract_code_blocks(message.content)
            # script = ('\n').join(script)
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
    return script, citations,output

def extract_code_blocks(text, language='python'):
    # Define the start and end markers for the code block
    start_marker = f"```{language}"
    end_marker = "```"
    code_blocks = []
    start_pos = 0

    while True:
        # Find the start position of the next code block
        start_pos = text.find(start_marker, start_pos)
        if start_pos == -1:
            break  # No more code blocks found

        # Move the start position to the end of the start marker
        start_pos += len(start_marker)

        # Find the end position of the code block
        end_pos = text.find(end_marker, start_pos)
        if end_pos == -1:
            break  # No end marker found, stop searching

        # Extract and append the code block
        code_block = text[start_pos:end_pos].strip()
        code_blocks.append(code_block)

        # Move the start position past the end marker for the next search
        start_pos = end_pos + len(end_marker)

    return code_blocks

def main():
    parser = argparse.ArgumentParser(description='Process a prompt for the LLM.')
    parser.add_argument('prompt', type=str, help='The prompt to send to the LLM')
    args = parser.parse_args()

    # Call the llm function with the provided prompt
    response = llm(args.prompt)
    print(response)

if __name__ == "__main__":
    # test("Hi!")
    
    question = 'Calculate the average fat content (in grams) for all foods in the "Groente" (vegetables) category.'
    llm(question)
    
    # question = 'Which vegetable in the dataset has the highest amount of vitamin C per 100 grams?'
    # llm(question)

    # main()