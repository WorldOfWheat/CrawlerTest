import tempfile

temp_folder = tempfile.gettempdir()

def write(filename, content) -> None:
    with open(f'{temp_folder}/{filename}', 'w') as f:
        f.write(content)

def read(filename) -> str:
    with open(f'{temp_folder}/{filename}', 'r') as f:
        return f.read()