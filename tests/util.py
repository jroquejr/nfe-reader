
def load_file(file_path):
    with open(f"tests/fixtures/{file_path}") as fo:
        return fo.read()