lang_file_encoding = 'latin-1'


class TextFormatter:
    def __init__(self, text_to_edit: bytes) -> None:
        self._text_to_edit: bytes = text_to_edit
        self._formatted_text_list: list[str]
        self._line_lengths: tuple[int, int]
        self._formatted_text_list, self._line_lengths = self._format_text()
        self._reformatted_text_list: list[bytes] = self._reformat_text()

    def _format_text(self) -> tuple[list[str], list[tuple[int, int]]]:
        res_text_list, lengths_list = [], []
        cur_line = ''
        while (cur_index := self._text_to_edit.find(b'\x00')) != -1:
            space_quantity = get_space_quantity(self._text_to_edit[cur_index + 1:])
            if space_quantity <= 3:
                remained_spaces = ''
                if space_quantity > 1:
                    remained_spaces = ' '
                cur_line += self._text_to_edit[:cur_index].decode(lang_file_encoding) + remained_spaces

            elif space_quantity > 3:
                additional_len = (space_quantity - 3) // 2
                cur_line += self._text_to_edit[:cur_index]
                add_line(res_text_list, cur_line, additional_len)
                lengths_list.append((len(cur_line), additional_len))
                cur_line = ''

            self._text_to_edit = self._text_to_edit[cur_index + space_quantity:]

        # обработка последней строки, если в конце неё нет пробелов
        if self._text_to_edit:
            cur_line += self._text_to_edit
            add_line(res_text_list, cur_line, 0)
            lengths_list.append((len(cur_line), 0))
        return res_text_list, lengths_list

    def _reformat_text(self) -> list[bytes]:
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
            res_text_list.append(edited_line.encode(encoding=lang_file_encoding))
        return res_text_list

    def get_formatted_text(self) -> str:
        return '\n'.join(self._formatted_text_list)

    def get_reformatted_text(self) -> bytes:
        return b''.join(self._reformatted_text_list)


def add_line(line_list: list[str], line: str, extra_len: int) -> None:
    line_list.append(
        line +
        f' (ORIGINAL LENGTH: {len(line)}, MAX LENGTH: {len(line) + extra_len})' +
        '\n'
    )


def get_space_quantity(line: str) -> int:
    space_quantity = 1
    for ltr in line:
        if ltr != ' ':
            break
        space_quantity += 1
    return space_quantity
