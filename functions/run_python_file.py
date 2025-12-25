import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a specified python file in a specified directory relative to the working directory. Optional arguments can be added to the call",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a python file which needs to be executed, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments that can be provided for running python file",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    common_path = os.path.commonpath([working_dir_abs, target_path])
    try:
        if common_path != working_dir_abs:
            error = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            print(error)
            return error
        full_path = os.path.normpath(os.path.join(working_directory, file_path))
        if os.path.isfile(full_path) is False:
            error = f'Error: "{file_path}" does not exist or is not a regular file'
            print(error)
            return error
        if full_path.endswith(".py") is False:
            error = f'Error: "{file_path}" is not a Python file'
            print(error)
            return error
        command = ["python", target_path]
        if args is not None:
            command.extend(args)
        result: subprocess.CompletedProcess = subprocess.run(
            command,
            timeout=30,
            text=True,
            stdout=True,
            stderr=True,
            cwd=working_dir_abs,
        )
        output_string = ""
        if result.returncode != 0:
            output_string = f"Process exited with code {result.returncode}"
        if result.stdout is None and result.stderr is None:
            output_string = "No output produced\n"
        output_string += f"STDOUT: {result.stdout}\n"
        output_string += f"STDERR: {result.stderr}\n"
        print(output_string)
        return output_string
    except Exception as e:
        error = f"Error: executing Python file: {e}"
        print(error)
        return error
