import os

def get_files_info(working_directory, directory=None):
    absdir = os.path.abspath(working_directory)
    fulldir = os.path.join(absdir, directory)

    if fulldir.startswith(absdir) == False:
       return print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

    if os.path.isdir(fulldir) == False:
        return print(f'Error: "{directory}" is not a directory')

    try:
        output = []
        for obj in os.listdir(fulldir):
            filepath = os.path.join(fulldir, obj)
            output.append(f"- {obj}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}")
        return "\n".join(output)
    except Exception as e:
        return f"Error listing files: {e}"