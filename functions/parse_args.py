import argparse
import sys
"""
PURPOSE: Parses and validates command-line arguments (sys.argv) for the agent. 
It uses the argparse module to extract the user's main 'prompt' and check 
for operational flags (like --verbose).

VALIDATION: Explicitly checks if the user's prompt contains internal spaces 
and fails if it is not wrapped in quotes, enforcing correct script execution syntax.
Returns the required prompt string, verbose state, and debug state.
"""
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="Prompt for the agent (must be wrapped in quotes)")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    raw_args = sys.argv[1:]
    flag_set = {"-v", "--verbose", "--debug"}
    non_flags = [a for a in raw_args if a not in flag_set]

    if len(non_flags) > 1:
        print(
            "Error: Prompt must be wrapped in quotes.\n"
            "Example:\n"
            '  uv run main.py "fix my calculator" --verbose'
        )
        sys.exit(1)

    return args.prompt, args.verbose, args.debug