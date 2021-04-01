import builtins
import sys
import tempfile
from pathlib import Path
from typing import List
from zipfile import ZipFile

from .execution_base import Exploit


class FilesystemPythonExploit(Exploit):
    category_name = "Filesystem Python Code Execution"


class ImportExploit(FilesystemPythonExploit):
    vulnerable_function = builtins.__import__  # Used by the 'import' keyword

    def generate_payload(source_code: str) -> List[str]:
        return [source_code, "helper.py"]

    def run_payload(payload: str, file_name: str) -> None:
        # Prevent path traversal
        if ".." in file_name or "/" in file_name:
            raise Exception(
                "Path traversal attempt. '..' and '/' not allowed in file name"
            )

        file_path = Path(__file__).parent / file_name

        if file_path.exists():
            raise Exception(f"{file_path} already exists. Can't overwrite it.")

        try:
            file_path.write_text(payload)

            from . import helper

            # Do stuff

        finally:
            # Clean up temp file
            file_path.unlink()


class EnvironmentVariableExploit(FilesystemPythonExploit):
    vulnerable_function = "sys.path.insert"

    def generate_payload(source_code: str) -> List[str]:
        return [
            source_code,
            "requests.py",
            str(Path(__file__).parent / "tmp/user_upload.zip"),
        ]

    def run_payload(
        zip_file_contents: str, zip_file_name: str, path_value: str
    ) -> None:
        # Simulate a user uploaded zip file
        temp_upload_zip = Path(__file__).parent / "tmp/user_upload.zip"
        temp_upload_zip.parent.mkdir()
        with ZipFile(str(temp_upload_zip), "w") as zip:
            zip.writestr(zip_file_name, zip_file_contents)

        try:
            sys.path.insert(0, path_value)

            import requests

            # Do stuff
        finally:
            # Clean up temp file
            temp_upload_zip.unlink()
            temp_upload_zip.parent.rmdir()
