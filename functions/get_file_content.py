import os
from google.genai import types

MAX_CHARS = 10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get content of a specified file in a specified directory relative to the working directory",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a file which content needs to be read, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    common_path = os.path.commonpath([working_dir_abs, target_dir])
    try:
        if common_path != working_dir_abs:
            error = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            print(error)
            return error
        full_path = os.path.join(working_directory, file_path)
        if os.path.isfile(full_path) is False:
            error = f'Error: File not found or is not a regular file: "{file_path}"'
            print(error)
            return error
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            print(file_content_string)
            return file_content_string
    except Exception as e:
        error = f"  Error: {e}"
        print(error)
        return error
