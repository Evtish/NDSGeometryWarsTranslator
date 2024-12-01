lang_file_encoding = 'latin-1'


def get_space_quantity(line: str) -> int:
    space_quantity = (line[:2] == '"!') + 1
    for ltr in line[2:]:
        if ltr != '\x00':
            if ltr == '!':
                space_quantity += 1
            break
        space_quantity += 1
    return space_quantity


def format_binary_file(original_text: str) -> tuple[list[str], list[tuple[int, int]]]:
    text_to_edit = original_text
    formatted_text_list, line_lengths = [], []

    def add_line(line: str, extra_len: int) -> None:
        formatted_text_list.append(
            line +
            f' (ORIGINAL LENGTH: {len(line)}, MAX LENGTH: {len(line) + extra_len})' +
            '\n'
        )

    # text_to_edit = text.replace('\x00', ' ')
    cur_index = text_to_edit.find('\x00')
    original_text_index = cur_index
    divider_quantity = 0
    cur_line = ''
    while cur_index != -1:
        divider_quantity = get_space_quantity(original_text[original_text_index - 2:])
        if divider_quantity < 3:
            # remained_spaces = ''
            # if divider_quantity > 1:
            #     remained_spaces = ' '
            cur_line += text_to_edit[:cur_index]

        elif divider_quantity >= 3:
            additional_len = (divider_quantity - 3) // 2

            cur_line += text_to_edit[:cur_index]
            add_line(cur_line, additional_len)
            line_lengths.append((len(cur_line), additional_len))

            cur_line = ''
        cur_index = text_to_edit.find('\x00')
        original_text_index += cur_index
        text_to_edit = text_to_edit[cur_index + divider_quantity:]

    # обработка последней строки, если в конце неё нет пробелов
    if text_to_edit or cur_line:
        additional_len = max(0, (divider_quantity - 3) // 2)
        cur_line = cur_line.rstrip(' ') + text_to_edit
        add_line(cur_line, additional_len)
        line_lengths.append((len(cur_line), additional_len))

    return formatted_text_list, line_lengths


def format_text_file(text_list: list[str], lengths_list: list[tuple[int, int]]) -> list[str]:
    reformatted_text_list = []
    for i, line in enumerate(text_list):
        line = line[:line.rfind('(') - 1]
        # edited_line = (
        #     line
        #     .replace('', '\x00')
        #     .lstrip('\x00')
        # )
        edited_line = ''
        for j in range(len(line)):
            separator = '\x00'
            if line[j] == '"' or line[j] == '!' and line[j - 1] == '"':
                separator = ''
            edited_line += line[j] + separator

        original_len, extra_len = lengths_list[i]
        empty_symbol_quantity = extra_len - len(line) + original_len

        edited_line += '\x00' * (empty_symbol_quantity * 2 + 2)
        reformatted_text_list.append(edited_line)

    return reformatted_text_list


if __name__ == '__main__':
    # with open('LangEN.bin', 'rb') as file1:
    #     file1_data = file1.read().decode(lang_file_encoding)
    #     text_start_index = file1_data.find('A\x00c\x00h\x00i\x00e\x00v\x00e\x00m\x00e\x00n\x00t\x00s')
    #     formatted_bin_file_list, lengths = format_binary_file(file1_data[text_start_index:])
    # with open('test.txt', 'w', encoding=lang_file_encoding) as file2:
    #     file2.write('\n'.join(formatted_bin_file_list))
    #     formatted_txt_file_list = format_text_file(formatted_bin_file_list, lengths)
    # with open('test.bin', 'wb') as file3:
    #     file3_data = file1_data[:text_start_index] + ''.join(formatted_txt_file_list)
    #     file3.write(file3_data.encode(lang_file_encoding))
    test_text = 'S\x00t\x00y\x00l\x00u\x00s\x00\x00\x00\x00\x00G\x00e\x00o\x00m\x00e\x00t\x00r\x00y\x00 \x00W\x00a\x00r\x00s\x00 \x00:\x00 \x00G\x00a\x00l\x00a\x00x\x00i\x00e\x00s\x00"!\x00\x00\x00\x00\x00\x00'
    formatted_bin_file_list, lengths = format_binary_file(test_text)
    formatted_txt_file_list = format_text_file(formatted_bin_file_list, lengths)
    print(''.join(formatted_txt_file_list))
