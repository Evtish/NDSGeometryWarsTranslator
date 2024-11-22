lang_file_encoding = 'latin-1'


class BinaryFormatter:
    def __init__(self, text: bytes) -> None:
        self._text = text.decode(lang_file_encoding)
        # кортежи в _line_lengths: оригинальная длина стоки, количество доп. символов
        self._formatted_text_list, self._line_lengths = self._format_text()
        self._reformatted_text_list = self._reformat_text()

    def _format_text(self) -> tuple[list[str], list[tuple[int, int]]]:
        res_text_list, lengths_list = [], []

        def add_line(line: str, extra_len: int) -> None:
            res_text_list.append(
                line +
                f' (ORIGINAL LENGTH: {len(line)}, MAX LENGTH: {len(line) + extra_len})' +
                '\n'
            )

        text_to_edit = self._text.replace('\x00', ' ')
        space_quantity = 0
        cur_line = ''
        while (cur_index := text_to_edit.find(' ')) != -1:
            space_quantity = get_space_quantity(text_to_edit[cur_index + 1:])
            if space_quantity <= 3:
                remained_spaces = ''
                if space_quantity > 1:
                    remained_spaces = ' '
                cur_line += text_to_edit[:cur_index] + remained_spaces

            elif space_quantity > 3:
                additional_len = (space_quantity - 3) // 2
                cur_line += text_to_edit[:cur_index]
                add_line(cur_line, additional_len)
                lengths_list.append((len(cur_line), additional_len))
                cur_line = ''

            text_to_edit = text_to_edit[cur_index + space_quantity:]

        # обработка последней строки, если в конце неё нет пробелов
        if text_to_edit or cur_line:
            additional_len = max(0, (space_quantity - 3) // 2)
            cur_line = cur_line.rstrip(' ') + text_to_edit
            add_line(cur_line, additional_len)
            lengths_list.append((len(cur_line), additional_len))
        return res_text_list, lengths_list

    def _reformat_text(self) -> list[str]:
        res_text_list = []
        for i, line in enumerate(self._formatted_text_list):
            line = line[:line.rfind('(') - 1]
            edited_line = (
                line
                .replace('', '\x00')
                .lstrip('\x00')
            )

            original_len, extra_len = self._line_lengths[i]
            empty_symbol_quantity = extra_len - len(line) + original_len

            edited_line += '\x00' * (empty_symbol_quantity * 2 + 2)
            res_text_list.append(edited_line)
        return res_text_list

    def get_formatted_text(self) -> str:
        return '\n'.join(self._formatted_text_list)

    def get_reformatted_text(self) -> str:
        return ''.join(self._reformatted_text_list)


def get_space_quantity(line: str) -> int:
    space_quantity = 1
    for ltr in line:
        if ltr != ' ':
            break
        space_quantity += 1
    return space_quantity


if __name__ == '__main__':
    with open('LangEN.bin', 'rb') as bin_file:
        text_formatter = BinaryFormatter(bin_file.read())
    with open('test.txt', 'w', encoding=lang_file_encoding) as txt_file:
        txt_file.write(text_formatter.get_formatted_text())
