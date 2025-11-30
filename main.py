import os
import sys
import argparse
from config import SYSTEM_PROMPT
from schema import schema_get_files_info
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    # print("Hello from bootdev-aigent-proj!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-001"
    if len(sys.argv) < 2:
        print("No prompt provided.\nTry --> uv run main.py \"your_prompt_here\"")
        sys.exit(1)    
    if len(sys.argv) > 2 and "--verbose" not in sys.argv:
        print("Remember to wrap your prompt in single or double quotes: \' or \"")
        sys.exit(1)   
    if len(sys.argv) > 3:
        print("Remember to wrap your prompt in single or double quotes: \' or \"")
        sys.exit(1)    
    if sys.argv[1] == "--verbose":
        contents = sys.argv[2]
    else:
        contents = sys.argv[1]
    if len(contents.strip()) == 0:
        print("Prompt is empty or contains only whitespace!\nTry again.")
        sys.exit(1)
    # Figure out which argument is the prompt
    if "--verbose" in sys.argv:
        print(f"User prompt: {contents}")
        # print(f"Prompt tokens: {iteration_tokens.prompt_token_count}")
        # print(f"Response tokens: {iteration_tokens.candidates_token_count}")
    messages = [
        types.Content(role="user", parts=[
            types.Part(text=contents)
        ])
    ]
    
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)  
    generated_content = client.models.generate_content(
        model=model, 
        contents=messages, 
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT
            )
        )
    gc_fc = generated_content.function_calls
    if gc_fc:
        for ea in gc_fc:
            print(f"Calling function: {ea.name}({ea.args})")
    else:
        print(generated_content.text)
    tokens_used = generated_content.usage_metadata
    if "--verbose" in sys.argv:
       print(f"Prompt tokens: {tokens_used.prompt_token_count}")
       print(f"Response tokens: {tokens_used.candidates_token_count}")

if __name__ == "__main__":
    main()

