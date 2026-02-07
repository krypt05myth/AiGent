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
# 1. Init the standard argparse machinery to handle flags and help menus.
    parser = argparse.ArgumentParser()
    # Define the core positional arg. Argparse expects this to be one string.
    parser.add_argument("prompt", help="Prompt for the agent (must be wrapped in quotes)")
    # Define boolean switches. Using 'store_true' means they default to False unless present.
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--debug", action="store_true")
    # Perform the initial parse. If -h or --help is used, the script ends here.
    args = parser.parse_args()
# 2. Manual Logic: The 'Space-Quote' Safety Net.
    # Argparse is too 'helpful' and will split unquoted strings into multiple arguments.
    # We grab the raw sys.argv (skipping the script name at index 0) to audit the shell's work.
    raw_args = sys.argv[1:]
    # We define a whitelist of flags to ignore during our audit.
    flag_set = {"-v", "--verbose", "--debug"}
    # Filter out the flags to see how many 'naked' positional strings were passed.
    non_flags = [a for a in raw_args if a not in flag_set]
    # If the shell passed more than one non-flag string, the user forgot their quotes.
    # Example: 'uv run main.py fix my code' results in ['fix', 'my', 'code'].
    # We kill the process immediately to prevent the agent from receiving a partial prompt.
    if len(non_flags) > 1:
        print(
            "Error: Prompt must be wrapped in quotes.\n"
            "Example:\n"
            '  uv run main.py "fix my calculator" --verbose'
        )
        sys.exit(1)
# 3. Return the sanitized state as a clean tuple for easy unpacking in main().
    return args.prompt, args.verbose, args.debug