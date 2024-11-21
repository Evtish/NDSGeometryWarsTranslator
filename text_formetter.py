def add_line(line_list: list[str], line: str, extra_len: int) -> None:
    line_list.append(
        line +
        f' (ORIGINAL LENGTH: {len(line)}, MAX LENGTH: {len(line) + extra_len})' +
        '\n'
    )


def get_spaces_quantity(line: str) -> int:
    spaces_quantity = 1
    for ltr in line:
        if ltr != ' ':
            break
        spaces_quantity += 1
    return spaces_quantity


class TextFormatter:
    def __init__(self, text: str) -> None:
        self.divider = '  '
        self.text_to_edit = text.rstrip(' ')
        self.formatted_text_list = self._format_text()
        self.unformatted_text_list = self._unformat_text()

    def _format_text(self) -> list[str]:
        cur_line = ''
        res_list = []
        while (cur_index := self.text_to_edit.find(' ')) != -1:
            total_spaces_count = get_spaces_quantity(self.text_to_edit[cur_index + 1:])
            if total_spaces_count <= len(self.divider) + 1:
                remained_spaces = ''
                if total_spaces_count > 1:
                    remained_spaces = ' '
                cur_line += self.text_to_edit[:cur_index] + remained_spaces

            elif total_spaces_count > len(self.divider) + 1:
                cur_line += self.text_to_edit[:cur_index]
                add_line(res_list, cur_line, (total_spaces_count - 3) // 2)
                cur_line = ''

            self.text_to_edit = self.text_to_edit[cur_index + total_spaces_count:]
        else:
            cur_line += self.text_to_edit
            add_line(res_list, cur_line, 0)
        return res_list

    def _unformat_text(self) -> list[bytes]:
        # res_text = (
        #     text
        #     .replace('', ' ')
        #     .strip(' ')
        #     .replace('\n', '   ')
        # )
        text_lines = self.text_to_edit.split('\n')
        for line in text_lines:
            pass

        cur_line = ''
        res_list = []
        while (cur_index := self.text_to_edit.find(' ')) != -1:
            total_spaces_count = get_spaces_quantity(self.text_to_edit[cur_index + 1:])
            if total_spaces_count <= len(self.divider) + 1:
                remained_spaces = ''
                if total_spaces_count > 1:
                    remained_spaces = ' '
                cur_line += self.text_to_edit[:cur_index] + remained_spaces

            elif total_spaces_count > len(self.divider) + 1:
                cur_line += self.text_to_edit[:cur_index]
                add_line(res_list, cur_line, (total_spaces_count - 3) // 2)
                cur_line = ''

            self.text_to_edit = self.text_to_edit[cur_index + total_spaces_count:]
        else:
            cur_line += self.text_to_edit
            add_line(res_list, cur_line, 0)
        return res_list

    def get_formatted_text(self) -> str:
        return '\n'.join(self.formatted_text_list)

    def get_unformatted_text(self) -> bytes:
        pass