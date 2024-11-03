__all__ = (
    'FileConverter',
    'get_file_extension',
    'get_all_files'
)

from os import PathLike, path, getcwd, listdir

ENCODING = 'cp1251'


class FileConverter:
    def __init__(self, filename: PathLike[bytes] | PathLike[str] | str) -> None:
        self.filename = filename

    def bin_to_txt(self, txt_filename: str) -> None:
        with open(self.filename, 'rb') as bin_file:
            bin_file_data = bin_file.read()

        # txt_file_data = ''.join(map(str, bin_file_data)) + '\n'
        txt_file_data = bin_file_data.decode(encoding=ENCODING)
        with open(txt_filename + '.txt', 'w', encoding=ENCODING) as txt_file:
            txt_file.write(txt_file_data)

    def txt_to_bin(self, bin_filename: str) -> None:
        with open(self.filename, 'r', encoding=ENCODING) as txt_file:
            txt_file_data = txt_file.read()

        bin_file_data = str.encode(txt_file_data, encoding=ENCODING)
        with open(bin_filename + '.bin', 'wb') as bin_file:
            bin_file.write(bin_file_data)


def get_file_extension(file: PathLike[bytes] | PathLike[str] | str) -> str:
    return path.splitext(file)[1][1:]


def get_all_files() -> list[PathLike[bytes] | PathLike[str] | str]:
    cur_dir = getcwd()
    all_files = [f for f in listdir(cur_dir) if path.isfile(path.join(cur_dir, f))]
    return list(filter(lambda f: get_file_extension(f) in ('bin', 'txt'), all_files))
