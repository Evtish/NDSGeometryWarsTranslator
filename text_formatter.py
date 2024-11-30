lang_file_encoding = 'latin-1'


def get_space_quantity(line: str) -> int:
    space_quantity = 1
    for ltr in line:
        if ltr != '\x00':
            break
        space_quantity += 1
    return space_quantity


def format_binary_file(text: str) -> tuple[list[str], list[tuple[int, int]]]:
    formatted_text_list, line_lengths = [], []

    def add_line(line: str, extra_len: int) -> None:
        formatted_text_list.append(
            line +
            f' (ORIGINAL LENGTH: {len(line)}, MAX LENGTH: {len(line) + extra_len})' +
            '\n'
        )

    # text_to_edit = text.replace('\x00', ' ')
    divider_quantity = 0
    cur_line = ''
    while (cur_index := text.find('\x00')) != -1:
        divider_quantity = get_space_quantity(text[cur_index + 1:])
        if divider_quantity < 3:
            # remained_spaces = ''
            # if divider_quantity > 1:
            #     remained_spaces = ' '
            cur_line += text[:cur_index]

        elif divider_quantity >= 3:
            additional_len = (divider_quantity - 3) // 2

            cur_line += text[:cur_index]
            add_line(cur_line, additional_len)
            line_lengths.append((len(cur_line), additional_len))

            cur_line = ''
        text = text[cur_index + divider_quantity:]

    # обработка последней строки, если в конце неё нет пробелов
    if text or cur_line:
        additional_len = max(0, (divider_quantity - 3) // 2)
        cur_line = cur_line.rstrip(' ') + text
        add_line(cur_line, additional_len)
        line_lengths.append((len(cur_line), additional_len))

    return formatted_text_list, line_lengths


def format_text_file(text_list: list[str], lengths_list: list[tuple[int, int]]) -> list[str]:
    reformatted_text_list = []
    for i, line in enumerate(text_list):
        line = line[:line.rfind('(') - 1]
        edited_line = (
            line
            .replace('', '\x00')
            .lstrip('\x00')
        )

        original_len, extra_len = lengths_list[i]
        empty_symbol_quantity = extra_len - len(line) + original_len

        edited_line += '\x00' * (empty_symbol_quantity * 2 + 2)
        reformatted_text_list.append(edited_line)

    return reformatted_text_list


if __name__ == '__main__':
    with open('LangEN.bin', 'rb') as file1:
        formatted_bin_file_list, lengths = format_binary_file(file1.read().decode(lang_file_encoding))
    with open('test.txt', 'w', encoding=lang_file_encoding) as file2:
        file2.write('\n'.join(formatted_bin_file_list))
        formatted_txt_file_list = format_text_file(formatted_bin_file_list, lengths)
    with open('test.bin', 'wb') as file3:
        file3.write(''.join(formatted_txt_file_list).encode(lang_file_encoding))
