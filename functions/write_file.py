import os

def write_file(working_directory: str, file_path: str, content: str):
    try:
        working_dir_abs = os.path.abspath(working_directory) # type: ignore #est the true, fixed working_dir boundary
        full_path_file = os.path.abspath(os.path.join(working_directory, file_path)) #joins incoming dir to work_dir, and then sets it as fixed/abs path
        #this checks that a full_path startswith the fixed/abs work_dir, because if not then it is out of bounds
        if not full_path_file.startswith(working_dir_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        #this checks that the incoming file_path, now part of full_path, is valid or leads to a valid full_path
        
        with open(full_path_file, "w") as f:
            #this structure returns the bytes/chars written            
            file_content_bytes = f.write(content)
        return f'Successfully wrote to "{file_path}" ({file_content_bytes} characters written)'
    except Exception as e:
        return f"Error: {e}"
