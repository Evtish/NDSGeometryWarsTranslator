from os import PathLike
from typing import TextIO, BinaryIO


class FileConverter:
    def __init__(self, filename: PathLike[bytes | str] | str) -> None:
        self.filename = filename

    def convert_bin_to_txt(self) -> TextIO:
        with open(self.filename, 'rb', encoding='utf-8') as bin_file:
            bin_file_data = bin_file.read()

        txt_filename = self.filename[:self.filename.rfind('.')] + '.txt'
        txt_file_data = ''.join(map(str, bin_file_data)) + '\n'
        with open(txt_filename, 'w', encoding='utf-8') as txt_file:
            txt_file.write(txt_file_data)

        return txt_file

    def convert_txt_to_bin(self) -> BinaryIO:
        with open(self.filename, 'r', encoding='utf-8') as txt_file:
            txt_file_data = txt_file.read()

        bin_filename = self.filename[:self.filename.rfind('.')] + '.bin'
        bin_file_data = str.encode(txt_file_data, 'utf-8')
        with open(bin_filename, 'wb', encoding='utf-8') as bin_file:
            bin_file.write(bin_file_data)

        return bin_file
