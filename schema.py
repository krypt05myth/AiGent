from google.genai import types
##Schemas and tooling definitions or API interfaces: schemas, types, db models - JSON schemas, tool decs, API models

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file, constrained to the working directory. Reads up to MAX_CHARS.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be read, relative to the working directory.",
            ),
        },
        required=["file_path"], # file_path is mandatory to read a specific file
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to a file, overwriting the file if it exists or creating it if it does not. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be written, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string content to be written to the file. This will overwrite existing contents."
            )
        },
        required=["file_path", "content"], # file_path is mandatory to read a specific file
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file (script) using the 'python3' interpreter and captures its standard output (STDOUT) and standard error (STDERR).",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be written, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY, #ARRAY is used... not LIST... for Schema decs!
                description="The list of arguments passed to the function or script being called.",
                items=types.Schema(type=types.Type.STRING) #must include this line to specify what the items' types in the ARRAY are
            )
        },
        required=["file_path"], # file_path is mandatory to execute a specific function/script file; args is optional!
    ),
)