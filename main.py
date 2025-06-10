import os, sys, getopt
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()

    if len(sys.argv) < 2:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [-v, --verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    prompt = sys.argv[1]
    args = sys.argv[2:]
    short_options = 'v'
    long_options = ['verbose']
    optlist, args = getopt.getopt(args, short_options, long_options)
    
    if any([opt[0]=='-v' or opt[0]=='--verbose' for opt in optlist]):
        def vprint(print_data):
            print(print_data)
    else:
        def vprint(print_data):
            pass
    
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001',
        contents = messages
    )
    vprint(f"User prompt:{messages}\n")
    print(f"Response: {response.text}")
    vprint(f"""Prompt tokens: {response.usage_metadata.prompt_token_count}
Response tokens: {response.usage_metadata.candidates_token_count}""")

if __name__ == "__main__":
    main()