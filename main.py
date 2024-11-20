from file_helper import *
from file_helper import format_text


def choose_working_file(working_files: list[LangFileType]) -> LangFileType:
    for i, filename in enumerate(working_files):
        print(f'{i + 1}. {filename}')

    # TODO: fix bug
    try:
        file_number = max(0, int(input('Write file number you would like to work: ')) - 1)
        return working_files[file_number]
    except (IndexError, ValueError):
        print('Incorrect file number.\n')
        choose_working_file(working_files)


def main() -> None:
    working_file = choose_working_file(get_all_files())
    working_file_converter = FileConverter(working_file)
    converted_file_name = input('Write name of converted file (without extension): ')

    match get_file_extension(working_file):
        case 'bin':
            working_file_converter.bin_to_txt(converted_file_name)
            print('Text file was created')
        case 'txt':
            text = 'A c h i e v e m e n t s         F o u n d   a   g a m e         '
            print(format_text(text))
            # working_file_converter.txt_to_bin(converted_file_name)
            # print('Binary file was created')


main()
