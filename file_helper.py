__all__ = (
    'LangFileType',
    'FileConverter',
    'get_file_extension',
    'get_all_files'
)

from os import PathLike, path, getcwd, listdir
from typing import TypeVar
from text_formatter import FileFormatter, lang_file_encoding

LangFileType = TypeVar('LangFileType', PathLike[bytes],  PathLike[str],  str)


class FileConverter:
    def __init__(self, filename: LangFileType) -> None:
        self._filename: LangFileType = filename
        # self._binary_file_data = self._read_binary_file()
        # self._text_file_data = self._read_text_file()
        self._byte_text_formatter: FileFormatter = FileFormatter(self._read_binary_file())

    def _read_binary_file(self) -> bytes:
        with open(self._filename, 'rb') as bin_file:
            return bin_file.read()

    def _read_text_file(self) -> str:
        with open(self._filename, 'r', encoding=lang_file_encoding) as txt_file:
            return txt_file.read()

    def bin_to_txt(self, txt_filename: str) -> None:
        formatted_text_file_data = self._byte_text_formatter.get_formatted_text()
        with open(txt_filename + '.txt', 'w', encoding=lang_file_encoding) as txt_file:
            txt_file.write(formatted_text_file_data)

    def txt_to_bin(self, bin_filename: str) -> None:
        formatted_binary_file_data = self._byte_text_formatter.get_reformatted_text()
        with open(bin_filename + '.bin', 'w') as bin_file:
            bin_file.write(formatted_binary_file_data)


def get_file_extension(file: LangFileType) -> str:
    return path.splitext(file)[1][1:]


def get_all_files() -> list[LangFileType]:
    cur_dir = getcwd()
    all_files = [f for f in listdir(cur_dir) if path.isfile(path.join(cur_dir, f))]
    return list(filter(lambda f: get_file_extension(f) in ('bin', 'txt'), all_files))
