import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args=[]):
    try:
        working_dir_abs = os.path.abspath(working_directory) # type: ignore #est the true, fixed working_dir boundary
        full_path_file = os.path.abspath(os.path.join(working_directory, file_path)) #joins incoming dir to work_dir, and then sets it as fixed/abs path
        #this checks that a full_path startswith the fixed/abs work_dir, because if not then it is out of bounds
        if not full_path_file.startswith(working_dir_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        #this checks that the incoming file_path, now part of full_path, is valid or leads to a valid full_path
        if not os.path.isfile(full_path_file):
            return f'Error: File "{file_path}" not found.'
        if not full_path_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        script_dir = os.path.dirname(full_path_file)
        
        interpreter_script = ["python3", full_path_file]
        command_to_run = interpreter_script + args
        #text=True saves need to manual decode stdout and stderr byte streams with ".decod('utf-8')"
        #check=False prevents raising CalledProcessError on a non-0 exit, so we can check returncode
        completed_process = subprocess.run(command_to_run, capture_output=True, cwd=script_dir, timeout=30, check=False, text=True)
        comp_proc_rc = completed_process.returncode
        comp_proc_parts = []
        #Check if nothing output and exited cleanly
        if (not completed_process.stdout and not completed_process.stderr and comp_proc_rc == 0):
            return "No output produced."
        #STDOUT and STDERR 
        comp_proc_parts.append(f"STDOUT: {completed_process.stdout}")
        comp_proc_parts.append(f"STDERR: {completed_process.stderr}")        
        #Returncode/Exit Code check  
        if comp_proc_rc != 0:
            comp_proc_parts.append(f"Process exited with code {comp_proc_rc}")

        return "\n".join(comp_proc_parts)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
