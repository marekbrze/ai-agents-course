import os
import argparse
from functions.call_functions import available_functions, call_function
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Couldn't read the API KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("Could't get Api response")
    if args.verbose:
        print(
            f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}"
        )
    if response.function_calls is not None:
        function_results = []
        for function_call in response.function_calls:
            function_call_result: types.Content = call_function(function_call)
            if (
                function_call_result.parts is None
                or len(function_call_result.parts) == 0
            ):
                raise Exception(f"Error when calling {function_call}")
            first_item = function_call_result.parts[0]
            if first_item.function_response is None:
                raise Exception("Function response is empty")
            if first_item.function_response.response is None:
                raise Exception("Response in function response is empty")
            function_results.append(first_item)
            print(f"-> {first_item.function_response.response}")


if __name__ == "__main__":
    main()
