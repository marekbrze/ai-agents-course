import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    common_path = os.path.commonpath([working_dir_abs, target_dir])
    print_dir = f"'{directory}'" if directory != "." else "current"
    print(f"Result for {print_dir} directory:")
    try:
        if common_path != working_dir_abs:
            error = f'  Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
            print(error)
            return error
        if os.path.isdir(target_dir) is False:
            error = f'  Error: "{directory}" is not a directory'
            print(error)
            return error
        return_string = ""
        for item in os.listdir(os.path.join(working_directory, directory)):
            full_path = os.path.join(working_directory, directory, item)
            return_string += f"  - {item}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}\n"
        print(return_string)
        return return_string
    except Exception as e:
        error = f"  Error: {e}"
        print(error)
        return error
