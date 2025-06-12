import os, sys, getopt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    system_prompt = """
    Answer as if you were Navi from The Legend of Zelda.
    You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    All paths you provide should be relative to the working directory (./calculator). You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. Do not try to provide a working directory, is this property is not provided, it wil list files in the working directory itself.",
                ),
            },
        ),
    )
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Returns the contents of a specified file, limited to 10,000 characters, and constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The location of the file to read from, relative to the working directory. Must be provided.",
                ),
            },
        ),
    )
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python",
        description="Runs the specified .py file using the python interpreter, constrained to files contained in the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The location of the file to run, relative to the working directory. Must be provided.",
                ),
            },
        ),
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Either overwrites an existing file or creates a new file at the location specified, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The location to create the new file, or if that file already exists the location of the file to overwrite, relative to the working directory. must be provided.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content which is to be written to the new file, or which will overwrite the existing file."
                )
            },
        ),
    )
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
    )

    if len(sys.argv) < 2:
        print("AI Code Assistant")
        print('Usage: python main.py "your prompt here" [-v, --verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    prompt = sys.argv[1]
    args = sys.argv[2:]
    short_options = 'v'
    long_options = ['verbose']
    optlist, args = getopt.getopt(args, short_options, long_options)

    if any([opt[0]=='-v' or opt[0]=='--verbose' for opt in optlist]):
        verbose = True
        def vprint(print_data):
            print(print_data)
    else:
        verbose = False
        def vprint(print_data):
            pass

    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    loop = 0
    while loop <= int(os.environ.get("MAXIMUM_LOOPS")):
        loop += 1
        response = client.models.generate_content(
            model = 'gemini-2.0-flash-001',
            contents = messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
        )
        if response.function_calls:
            for candidate in response.candidates:
                messages.append(candidate.content)
            vprint(f"User prompt:{messages}\n")
            for call in response.function_calls:
                call_result = call_function(call, verbose)
                if not call_result.parts or not hasattr(call_result.parts[0], "function_response"):
                    raise Exception("Error: No function response in types.Content result")
                vprint(f"-> {call_result.parts[0].function_response.response['result']}")
            vprint(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
            messages.append(call_result)
        elif not response.function_calls:
            vprint(f"User prompt:{messages}\n")
            print(f"Response: {response.text}")
            vprint(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
            break
        elif loop == 21:
            vprint(f"User prompt:{messages}\n")
            print(f"Maximum number of loops exceeded and execution was halted.")
            vprint(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
            break

if __name__ == "__main__":
    main()