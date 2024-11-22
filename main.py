from file_helper import *
from pathlib import Path
# from text_formatter import TextFormatter


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
    converted_file_name = input(
        '''Write name of converted file without extension.
You can just press Enter, then file will be named as the original: '''
    )
    if not converted_file_name:
        converted_file_name = Path(working_file).stem

    match get_file_extension(working_file):
        case 'bin':
            # print(text_formatter.get_formatted_text())
            working_file_converter.bin_to_txt(converted_file_name)
            print('Text file was created')
        case 'txt':
            # print(text_formatter.get_reformatted_text())
            working_file_converter.txt_to_bin(converted_file_name)
            print('Binary file was created')


main()
