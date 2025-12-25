import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file in a specified directory relative to the working directory.",
    parameters=types.Schema(
        required=["file_path", "content"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a file that we want to write to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that needs to be written to the file",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    common_path = os.path.commonpath([working_dir_abs, target_dir])
    try:
        if common_path != working_dir_abs:
            error = f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            print(error)
            return error
        full_path = os.path.normpath(os.path.join(working_directory, file_path))
        if os.path.isdir(full_path) is True:
            error = f'Error: Cannot write to "{file_path}" as it is a directory'
            print(error)
            return error
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
            info = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            print(info)
            return info
    except Exception as e:
        error = f"  Error: {e}"
        print(error)
        return error
