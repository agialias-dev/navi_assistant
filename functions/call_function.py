from google.genai import types
from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .run_python import run_python_file
from .write_file import write_file

working_dir = {"working_directory": "./calculator"}

def call_function(function_call_part, verbose=False):
    func_name = function_call_part.name
    func_args = {**working_dir, **function_call_part.args}
    func_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python": run_python_file,
        "write_file": write_file
        }
    
    if func_name not in func_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )
    
    elif verbose == True:
        print(f"Calling function: {func_name}({func_args})")
    else:
        print(f" - Calling function: {func_name}")
    
    func_result = func_dict[func_name](**func_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": func_result},
            )
        ],
    )