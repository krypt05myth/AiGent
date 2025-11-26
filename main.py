import os
import sys 
from dotenv import load_dotenv
from google import genai


def main():
    # print("Hello from bootdev-aigent-proj!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    # contents = "Why is Boot.dev such a great place to learn backend development?" \
    # "Use one paragraph maximum."
    if len(sys.argv) < 2:
        print("No prompt provided.\nTry --> uv run main.py \"your_prompt_here\"")
        sys.exit(1)    
    contents = sys.argv[1]
    if len(sys.argv) > 2:
        print("Remember to wrap your prompt in single or double quotes: \' or \"")
        sys.exit(1)    
    if len(contents.strip()) == 0:
        print("Prompt is empty or contains only whitespace!\nTry again.")
        sys.exit(1)    
    generated_content = client.models.generate_content(model=model, contents=contents)

    print(generated_content.text)

    tokens_used = generated_content.usage_metadata
    print(f"Prompt tokens: {tokens_used.prompt_token_count}")
    print(f"Response tokens: {tokens_used.candidates_token_count}")

if __name__ == "__main__":
    main()

