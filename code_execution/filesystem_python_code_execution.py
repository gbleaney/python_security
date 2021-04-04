import builtins
import importlib
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple
import zipfile
import shutil
from .execution_base import Exploit
from .python_code_execution import PythonExploit
from werkzeug.datastructures import FileStorage
import io

class FilesystemPythonExploit(PythonExploit):
    category_name = "Filesystem Python Code Execution"


class UserControlledFileNameImportExploit(FilesystemPythonExploit):
    vulnerable_function = builtins.__import__  # Used by the 'import' keyword

    def generate_payload(source_code: str) -> FileStorage:
        return FileStorage(io.BytesIO(bytes(source_code,'ascii')), "helper.py")

    def run_payload(file_upload: FileStorage) -> None:
        file_name = file_upload.filename

        # Prevent path traversal
        if ".." in file_upload.filename or "/" in file_upload.filename:
            raise Exception(
                "Path traversal attempt. '..' and '/' not allowed in file name"
            )

        file_path = Path(__file__).parent / file_upload.filename

        if file_path.exists():
            raise Exception(f"{file_path} already exists. Can't overwrite it.")

        try:
            file_upload.save(file_path)

            from . import helper

            # Do stuff

        finally:
            # Clean up temp file
            file_path.unlink()


class UserControlledImportNameImportExploit(FilesystemPythonExploit):
    vulnerable_function = importlib.import_module

    def generate_payload(source_code: str) -> Tuple[FileStorage, str]:
        return (FileStorage(io.BytesIO(bytes(source_code,'ascii')), "__init__.py"), "tmp")

    def run_payload(file_upload: FileStorage, import_name: str) -> None:
        # Prevent path traversal
        if ".." in file_upload.filename or "/" in file_upload.filename:
            raise Exception(
                "Path traversal attempt. '..' and '/' not allowed in file name"
            )

        # Simulate a user uploaded temp file
        temp_folder = Path(__file__).parent.parent / "tmp"
        temp_folder.mkdir()
        temp_file = temp_folder / file_upload.filename

        file_upload.save(temp_file)

        try:
            importlib.import_module(import_name)

            # Do stuff
        finally:
            # Clean up temp files
            shutil.rmtree(str(temp_folder))


class EnvironmentVariableExploit(FilesystemPythonExploit):
    vulnerable_function = "sys.path.insert"

    def generate_payload(source_code: str) -> Tuple[FileStorage, str]:
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zip_file:
            zip_file.writestr("requests.py", source_code)
        memory_file.seek(0)

        return (FileStorage(memory_file, "user_upload.zip"), str(Path(__file__).parent.parent / "tmp/user_upload.zip"))

    def run_payload(
        zip_file_upload: FileStorage, path_value: str
    ) -> None:
        # Ensure upload is (named as) a zip file
        if not zip_file_upload.filename.endswith(".zip"):
            raise Exception(
                "Please upload a zip file"
            )

        # Save file to temp folder
        temp_folder = Path(__file__).parent.parent / "tmp"
        temp_folder.mkdir()
        temp_upload_zip = temp_folder / "user_upload.zip"

        zip_file_upload.save(temp_upload_zip)

        try:
            sys.path.insert(0, path_value)

            import requests

            # Do stuff
        finally:
            # Clean up temp files
            shutil.rmtree(str(temp_folder))
