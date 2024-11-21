__all__ = (
    'LangFileType',
    'FileConverter',
    'get_file_extension',
    'get_all_files'
)

from os import PathLike, path, getcwd, listdir
from typing import TypeVar
from text_formetter import format_text

LangFileType = TypeVar('LangFileType', PathLike[bytes],  PathLike[str],  str)
lang_file_encoding = 'utf-8'


class FileConverter:
    def __init__(self, filename: LangFileType) -> None:
        self.filename = filename

    def bin_to_txt(self, txt_filename: str) -> None:
        with open(self.filename, 'rb') as bin_file:
            bin_file_data = bin_file.read()

        txt_file_data = format_text(bin_file_data)
        with open(txt_filename + '.txt', 'wb') as txt_file:
            txt_file.write('\n'.encode(encoding=lang_file_encoding).join(txt_file_data))

    def txt_to_bin(self, bin_filename: str) -> None:
        with open(self.filename, 'rb') as txt_file:
            txt_file_data = txt_file.read()

        # bin_file_data = bytes(txt_file_data).decode(encoding=lang_file_encoding, errors='ignore')
        bin_file_data = txt_file_data.replace(
            ' '.encode(encoding=lang_file_encoding),
            chr(0).encode(encoding=lang_file_encoding)
        )
        with open(bin_filename + '.bin', 'wb') as bin_file:
            bin_file.write(bin_file_data)


def get_file_extension(file: LangFileType) -> str:
    return path.splitext(file)[1][1:]


# def get_binary_code(file_bytes: bytes) -> str:
#     return ''.join(str(file_bytes))[2:-1].replace('\\x00' * 2, '\n')


def get_all_files() -> list[LangFileType]:
    cur_dir = getcwd()
    all_files = [f for f in listdir(cur_dir) if path.isfile(path.join(cur_dir, f))]
    return list(filter(lambda f: get_file_extension(f) in ('bin', 'txt'), all_files))
