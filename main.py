import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import SYSTEM_PROMPT
from schema import schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file
from functions.call_function import call_function

def main():
    # print("Hello from bootdev-aigent-proj!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Error: No API Key provided.")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"  ##originally had gemini-2.0-flash-001, but randomly inserted lesson after 88% completion changed to this version!!
    is_verbose = False
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
        is_verbose = True
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
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)  
    generated_content = client.models.generate_content(
        model=model, 
        contents=messages,  ##Added to complete rando inserted lesson after 88% completion of course--> "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",  
        config=types.GenerateContentConfig(
           tools=[available_functions],
           system_instruction=SYSTEM_PROMPT
            )
        )
    
    tokens_used = generated_content.usage_metadata
    if tokens_used is None:
        raise RuntimeError("Error: No usage metadata; perhaps failed API call.")
    if "--verbose" in sys.argv:
        # Use getattr with defaults in case fields are missing
        # prompt_tokens = getattr(tokens_used, "prompt_token_count", 0)
        # response_tokens = getattr(tokens_used, "candidates_token_count", 0)
        print(f"Prompt tokens: {tokens_used.prompt_token_count}")
        print(f"Response tokens: {tokens_used.candidates_token_count}")
    ##was needed to complete the randomly inserted lesson that came when i was 88% finished with the whole course!
    # print(f"Prompt tokens: {tokens_used.prompt_token_count}")
    # print(f"Response tokens: {tokens_used.candidates_token_count}")
    
    gc_fc = generated_content.function_calls
    fn_responses = []
    if gc_fc:
        for fc in gc_fc:
            # print(f"Calling function: {ea.name}({ea.args})")
            fc_result = call_function(fc, verbose=is_verbose)
            if not fc_result.parts[0].function_response.response:
                raise Exception(f"Error: Function {fc.name} returned incomplete.")
            else:
                fn_responses.append(fc_result.parts[0])
            if is_verbose:
                print(f"-> {fc_result.parts[0].function_response.response}")
    else:
        print(f"Response:\n{generated_content.text}")


if __name__ == "__main__":
    main()
