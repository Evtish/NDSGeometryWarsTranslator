def format_text(text: str) -> str:
    found_val = '  '
    cur_line = ''
    res_text = []
    while (cur_index := text.find(' ')) != -1:
        total_spaces_count = 1
        for ltr in text[cur_index + 1:]:
            if ltr != ' ':
                break
            total_spaces_count += 1

        if total_spaces_count <= len(found_val) + 1:
            remained_spaces = ''
            if total_spaces_count > 1:
                remained_spaces = ' '

            cur_line += text[:cur_index] + remained_spaces
        elif total_spaces_count > len(found_val) + 1:
            additional_len = (total_spaces_count - 3) // 2
            cur_line += text[:cur_index]

            # TODO: add line length
            res_text.append(
                    cur_line +
                    f' (ORIGINAL LENGTH: {len(cur_line)}, MAX LENGTH: {len(cur_line) + additional_len})' +
                    '\n'
            )
            cur_line = ''

        text = text[cur_index + total_spaces_count:]
    return '\n'.join(res_text)


# def unformat_text(text: str) -> str:
#     # found_val = '  '
#     # res_text = (
#     #     text
#     #     .replace('', ' ')
#     #     .strip(' ')
#     #     .replace('\n', '   ')
#     # )
#     text_lines = text.split('\n')
#     for line in text_lines:
#         pass
#
#     while (cur_index := text.find(' ')) != -1:
#         total_spaces_count = 1
#         for ltr in text[cur_index + 1:]:
#             if ltr != ' ':
#                 break
#             total_spaces_count += 1
#
#         if total_spaces_count <= len(found_val) + 1:
#             remained_spaces = ''
#             if total_spaces_count > 1:
#                 remained_spaces = ' '
#
#             res_text += (
#                     text[:cur_index] +
#                     remained_spaces
#             )
#         elif total_spaces_count > len(found_val) + 1:
#             additional_len = (total_spaces_count - 3) // 2
#             cur_str = text[:cur_index]
#
#             # TODO: add line length
#             res_text += (
#                     cur_str +
#                     f' (letters can be added: {additional_len})' +
#                     '\n'
#             )
#
#         text = text[cur_index + total_spaces_count:]
#     return res_text