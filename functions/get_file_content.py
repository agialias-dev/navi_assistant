import os

def get_file_content(working_directory, file_path):
    absdir = os.path.abspath(working_directory)
    fullpath = os.path.join(absdir, file_path)

    if not fullpath.startswith(absdir):
        return f'Error: Cannot read "{file_path}"" as it is outside the permitted working directory'

    if not os.path.isfile(fullpath):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    try:
        with open(fullpath, 'r') as f:
            file_contents = f.read(MAX_CHARS)
    
        return file_contents
    except Exception as e:
        return f'Error: Could not read file "{file_path}": {str(e)}'