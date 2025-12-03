import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import SYSTEM_PROMPT, MAX_ITERS
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
        user_prompt = sys.argv[2]
    else:
        user_prompt = sys.argv[1]
    if len(user_prompt.strip()) == 0:
        print("Prompt is empty or contains only whitespace!\nTry again.")
        sys.exit(1)
    # Figure out which argument is the prompt
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        is_verbose = True
        # print(f"Prompt tokens: {iteration_tokens.prompt_token_count}")
        # print(f"Response tokens: {iteration_tokens.candidates_token_count}")
    messages = [
        types.Content(role="user", parts=[
            types.Part(text=user_prompt)
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

    # first_turn = True # Flag to handle the initial run case
    # while True:
    for iteration in range(MAX_ITERS): 
        # if not first_turn:
        '''
        if iteration > 0: #checking same as if not first_turn, so first_turn == False 
            user_prompt_next = input(f"What's your next prompt? Quit or Exit to leave.\nIteration count is: {iteration}")
            if user_prompt_next.lower() == "quit" or user_prompt_next.lower() == "exit":
                break
            messages.append(types.Content(
                role="user",
                parts=[types.Part(text=user_prompt_next)]
                )
            )
        '''
        try:
            generated_content = client.models.generate_content(
                model=model, 
                contents=messages,  ##Added to complete rando inserted lesson after 88% completion of course--> "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",  
                config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=SYSTEM_PROMPT
                    )
                )
        except Exception as e:
            print(f"Error during API call at iteration {iteration}: {e}")
            break
        tokens_used = generated_content.usage_metadata
        if tokens_used is None:
            raise RuntimeError("Error: No usage metadata; perhaps failed API call.")
        if is_verbose:
            # Use getattr with defaults in case fields are missing
            # prompt_tokens = getattr(tokens_used, "prompt_token_count", 0)
            # response_tokens = getattr(tokens_used, "candidates_token_count", 0)
            print(f"Prompt tokens: {tokens_used.prompt_token_count}")
            print(f"Response tokens: {tokens_used.candidates_token_count}")
        ##was needed to complete the randomly inserted lesson that came when i was 88% finished with the whole course!
        # print(f"Prompt tokens: {tokens_used.prompt_token_count}")
        # print(f"Response tokens: {tokens_used.candidates_token_count}")
        
        gc_fc = generated_content.function_calls
        # fn_responses = [] # This is where you store results from executed tools
        ##This could be a termination point
        model_response_text = generated_content.text
        if model_response_text and not gc_fc:
            print(f"Final response:\n{model_response_text}")
            break
        ##Tool execution logic
        if gc_fc: # This checks if the list of function_calls is NOT empty
            ##Tool requests get appended to messages
            for candidate in generated_content.candidates:
                messages.append(candidate.content)
            ##Execution of requested tools
            for fc in gc_fc:
                # messages.append(types.Content(role="model", parts=[types.Part.from_function_call(fc)])) # append model's tool request, execute, append tool result
                # print(f"Calling function: {ea.name}({ea.args})")
                fc_result = call_function(fc, verbose=is_verbose)
                # messages.append(fc_result) #fc_result is already a types.Content object, perfectly formatted for messages[]
                if not fc_result.parts[0].function_response.response:
                    raise Exception(f"Error: Function {fc.name} returned incomplete.")
                messages.append(fc_result) #fc_result is already a types.Content object, perfectly formatted for messages[]
                # else: # If function_calls is empty, it must be a text response
                    # fn_responses.append(fc_result.parts[0])
                if is_verbose:
                    print(f"-> {fc_result.parts[0].function_response.response}")
        ##This is for no tools called and should be covered in the earlier termination check
        else:
            print(f"Response:\n{generated_content.text}")
            messages.append(types.Content(role="model", parts=[types.Part(text=generated_content.text)])) # appened model's text to messages[]
        # first_turn = False # After the first turn, set this flag to False
        if iteration == MAX_ITERS - 1:
            print("\nMAX ITERATIONS REACHED -- Agent halted before providing final text response.")
            break

if __name__ == "__main__":
    main()
