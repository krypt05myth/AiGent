import os
from config import MAX_CHARS
"""
PURPOSE: Reads and returns the textual content of a single file. 
It includes safeguards for file existence and size limitation.

SECURITY: Enforces the working_directory boundary check and verifies 
that the path points to a regular file (os.path.isfile). It uses 
with open(...) to ensure safe automatic file closing and reads up to 
MAX_CHARS (10000) with a truncation warning to prevent resource exhaustion 
on large files.
"""
def get_file_content(working_directory: str, file_path: str):
    try:
        working_dir_abs = os.path.abspath(working_directory) # type: ignore #est the true, fixed working_dir boundary
        full_path_file = os.path.abspath(os.path.join(working_directory, file_path)) #joins incoming dir to work_dir, and then sets it as fixed/abs path
        #this checks that a full_path startswith the fixed/abs work_dir, because if not then it is out of bounds
        if not full_path_file.startswith(working_dir_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'    
        #this checks that the incoming file_path, now part of full_path, is valid or leads to a valid full_path
        if not os.path.isfile(full_path_file):
            return f'Error: "File not found or is not a regular file: {file_path}"'
        
        with open(full_path_file, "r") as f:
            file_content_str = f.read(MAX_CHARS) 
            if len(file_content_str) == MAX_CHARS and f.read(1):
                file_content_str += f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_str # type: ignore
    except Exception as e:
        return f"Error: {e}"