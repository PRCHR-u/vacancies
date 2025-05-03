from typing import Optional
import os


def _delete_file_content(filename: str):
    """
    Deletes all content from a specified file.

    Args:
        filename (str): The name of the file to clear.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: For any other error that occurs during file deletion.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            pass
    except Exception as e:
        _handle_file_error(filename, e, "deleting data")



def _handle_file_error(filename: str, e: Exception, action: str):
    """
    Handles errors that occur during file operations.

    Args:
        filename (str): The name of the file that was being operated on.
        e (Exception): The exception that occurred.
        action (str): A description of the action being performed (e.g., "reading", "writing").
    """


    print(f"An error occurred while {action} file")


def _read_file_content(filename: str) -> Optional[str]:
    """
    Reads the content of a file.

    Args:
        filename (str): The name of the file to read.

    Returns:
        Optional[str]: The content of the file as a string if the file exists and can be read,
                       None otherwise.

    Raises:
        Exception: If any error occurs during the file reading process.
    """

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        _handle_file_error(filename, e, "reading")
        return None