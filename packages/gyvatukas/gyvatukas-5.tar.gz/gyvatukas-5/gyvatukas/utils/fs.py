import os


def dir_exists(path: str) -> bool:
    result = os.path.isdir(path)
    return result


def file_exists(path: str) -> bool:
    result = os.path.isfile(path)
    return result


def write_file(path: str, content: str, override: bool = False) -> bool:
    if not override and file_exists(path):
        return False

    with open(path, "w") as f:
        f.write(content)

    return True


def read_file(path: str) -> str | None:
    if file_exists(path):
        with open(path, "r") as f:
            return f.read()
    return None

# TODO: get_filenames_in_dir(path: str, recursive: bool = False, abspath: bool = False) -> list[str]