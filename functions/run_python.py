import os, subprocess

def run_python_file(working_directory, file_path):
    absdir = os.path.abspath(working_directory)
    fullpath = os.path.normpath(os.path.join(absdir, file_path))
    fulldir = os.path.dirname(fullpath)

    if not fullpath.startswith(absdir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(fullpath):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        proc = subprocess.run(["python", fullpath], timeout=30, capture_output=True)
        stdout= proc.stdout.decode('utf-8').strip()
        stderr = proc.stderr.decode('utf-8').strip()
        if proc.returncode != 0:
            return f"Process exited with code {proc.returncode}\nSTDOUT:{stdout}\nSTDERR:{stderr}"
        elif len(stdout) == 0 and len(stderr) == 0:
            return "No output produced."
        else:
            return f"STDOUT:{stdout}\nSTDERR:{stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"