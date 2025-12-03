from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
"""
PURPOSE: Acts as the intermediary (dispatcher) between the AI model's function call 
request and the actual executable Python functions (tools). It maps the function 
name (string) from the model to the corresponding local Python function object.

SECURITY: Inject the 'working_directory' parameter into the arguments provided 
by the model. This is critical because the model does not have direct knowledge 
of the secure execution path, ensuring all file system operations are constrained 
to the defined sandbox (e.g., './calculator').
"""
def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    ## updating the fcp_args_dict with the ONE new value for the lesson's purposes after copying fcp.args as it is a 'special dict'
    fcp_args_dict = function_call_part.args.copy()
    fcp_args_dict.update({"working_directory":"./calculator"}) 
    functs_dict = {"get_files_info":get_files_info,"get_file_content":get_file_content, "write_file":write_file, "run_python_file":run_python_file}
    if function_call_part.name not in functs_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ]
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": functs_dict[function_call_part.name](**fcp_args_dict)},
                )
            ],
        )