__all__ = (
    'LangFileType',
    'FileConverter',
    'get_file_extension',
    'get_all_files'
)

from os import PathLike, path, getcwd, listdir
from typing import TypeVar

LangFileType = TypeVar('LangFileType', PathLike[bytes],  PathLike[str],  str)
lang_file_encoding = 'utf-8'


class FileConverter:
    def __init__(self, filename: LangFileType) -> None:
        self.filename = filename

    def bin_to_txt(self, txt_filename: str) -> None:
        with open(self.filename, 'rb') as bin_file:
            bin_file_data = bin_file.read()

        # txt_file_data = ''.join(map(str, bin_file_data)) + '\n'
        # txt_file_data = bin_file_data.decode(encoding=lang_file_encoding)
        with open(txt_filename + '.txt', 'wb') as txt_file:
            txt_file.write(bin_file_data)

    def txt_to_bin(self, bin_filename: str) -> None:
        with open(self.filename, 'rb') as txt_file:
            txt_file_data = txt_file.read()

        # bin_file_data = str.encode(txt_file_data, encoding=lang_file_encoding)
        with open(bin_filename + '.bin', 'wb') as bin_file:
            bin_file.write(txt_file_data)


def get_file_extension(file: LangFileType) -> str:
    return path.splitext(file)[1][1:]


def get_all_files() -> list[LangFileType]:
    cur_dir = getcwd()
    all_files = [f for f in listdir(cur_dir) if path.isfile(path.join(cur_dir, f))]
    return list(filter(lambda f: get_file_extension(f) in ('bin', 'txt'), all_files))
