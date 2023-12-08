import os

def verify_file_extension(filename, allowed_extensions):
    """
    Verify if the given filename has an allowed extension.

    Parameters:
    - filename (str): The name of the file to be verified.
    - allowed_extensions (list): A list of allowed extensions (e.g., ['.txt', '.jpg', '.png']).

    Returns:
    - bool: True if the file has an allowed extension, False otherwise.
    """
    # Get the file extension
    _, file_extension = os.path.splitext(filename)

    # Check if the file extension is in the list of allowed extensions
    return file_extension.lower() in allowed_extensions

# Example usage:
if __name__ == "__main__":
    filename = "example.txt"
    allowed_extensions = ['.txt', '.pdf', '.docx']

    if verify_file_extension(filename, allowed_extensions):
        print(f"The file '{filename}' has an allowed extension.")
    else:
        print(f"The file '{filename}' has an unsupported extension.")