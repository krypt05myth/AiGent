import os
"""
PURPOSE: Retrieves a list of files and directories within a specified path 
relative to the working directory. It gathers file size and directory status 
for each entry.

SECURITY: Uses absolute path resolution (os.path.abspath) and a critical
boundary check (full_path.startswith(working_dir_abs)) to prevent directory
traversal attacks (e.g., '..'-based attempts to access files outside the 
allowed 'working_directory' sandbox).
"""
def get_files_info(working_directory: str, directory: str="."):
    try:
        working_dir_abs = os.path.abspath(working_directory) #est the true, fixed working_dir boundary
        full_path = os.path.abspath(os.path.join(working_directory, directory)) #joins incoming dir to work_dir, and then sets it as fixed/abs path
        #this checks that a full_path startswith the fixed/abs work_dir, because if not then it is out of bounds
        if not full_path.startswith(working_dir_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        #this checks that the incoming dir, now part of full_path, is valid or leads to a valid full_path
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        entries = os.listdir(full_path)
        lines = []
        for entry in entries:
            entry_path = os.path.join(full_path, entry)
            entry_size = os.path.getsize(entry_path)
            entry_isdir = os.path.isdir(entry_path)
            lines.append(f"- {entry}: file_size={entry_size} bytes, is_dir={entry_isdir}") # type: ignore
        return "\n".join(lines) # type: ignore
    except Exception as e:
        return f"Error: {e}"