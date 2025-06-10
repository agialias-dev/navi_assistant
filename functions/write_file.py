import os

def write_file(working_directory, file_path, content):
    absdir = os.path.abspath(working_directory)
    fullpath = os.path.join(absdir, file_path)
    fulldir = os.path.dirname(fullpath)

    if not fullpath.startswith(absdir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.exists(fullpath) and os.path.isdir(fullpath):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        if not os.path.exists(fulldir):
            os.makedirs(os.path.dirname(fulldir), exist_ok=True)

        with open(fullpath, mode='x') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written).'
    except FileExistsError:
        with open(fullpath, mode='w') as f:
            f.write(content)
        return f'"{file_path}" already exists, content has been sucessfully overwritten ({len(content)} characters written).'
    except Exception as e:
        return f'Error: {str(e)}'