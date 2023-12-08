# from style import style
from style import Color

color = Color()


def markup(arg, markup):
    if markup.lower() == "blue":
        return color.Blue(arg)
    if markup.lower() == "red":
        return color.Red(arg)
    if markup.lower() == "green":
        return color.Green(arg)
    if markup.lower() == "yellow":
        return color.Yellow(arg)
    if markup.lower() == "magenta":
        return color.Magenta(arg)
    if markup.lower() == "cyan":
        return color.Cyan(arg)
    if markup.lower() == "white":
        return color.White(arg)
    if markup.lower() == "underline":
        return color.Underline(arg)
    if markup.lower() == "bold":
        return color.Bold(arg)
    if markup.lower() == "italic":
        return color.Italic(arg)


def table(data, config='', header_config='', word_space=2):
    """ data = [
            {"Name": ["Foo", "Fooo", "Fooooo"]},
            {"Surname": ["Bar", "Baar", "Baaar"]},
            {"Gender": ["Male", "Female", "Male"]
        }

    config = ["red", "green", "yellow", "blue", "magenta", "cyan", "white", "underline", "bold", "italy"]
    """
    chars = {
        'top': '─',
        'top-mid': '┬',
        'top-left': '┌',
        'top-right': '┐',
        'bottom': '─',
        'bottom-mid': '┴',
        'bottom-left': '└',
        'bottom-right': '┘',
        'left': '│', 'left-mid':
        '├', 'mid': '─',
        'mid-mid': '┼',
        'right': '│',
        'right-mid': '┤',
        'middle': '│'
    }

    rows = []
    table_header = ""
    row_list = []
    header_len = 0
    loop_count = 0
    header_list = []
    max_len_list = []
    header_top_line = ""
    table_bottom_line = ""
    header_bottom_line = ""
    table_row = ""
    loop_start = False
    sec_loop_count = 0
    temp_table_row = ""

    for i in data:
        current_key = list(i.keys())[0]
        max_len_list.append(
            {current_key: [len(list(data[loop_count].keys())[0])]})

        for x in i[current_key]:
            max_len_list[loop_count][current_key].append(len(x))
        row_list.append(list(data[loop_count][current_key]))

        loop_count += 1

    loop_count = 0

    for i in data:
        header_list.append(list(i.keys())[0])

    for i in header_list:
        temp_table_row = i
        for conf in header_config:
            sec_text = markup(temp_table_row, conf)
            temp_table_row = sec_text

        header_len = header_len + \
            len(i) + (word_space * 2 +
                      (max(max_len_list[loop_count][i]) - len(i)))
        table_header += (" " * word_space) + \
            temp_table_row + (" " * (word_space +
                                     (max(max_len_list[loop_count][i]) - len(i)))) + chars["right"]
        temp_table_row = ""

        header_top_line += chars["top"] * (len((" " * word_space) +
                                               i + (" " * (word_space +
                                                    (max(max_len_list[loop_count][i]) - len(i)))) + chars["top-right"]) - 1)

        header_bottom_line += chars["bottom"] * (len((" " * word_space) +
                                                     i + (" " * (word_space +
                                                          (max(max_len_list[loop_count][i]) - len(i)))) + chars["right"]) - 1)
        table_bottom_line += chars["bottom"] * (len((" " * word_space) +
                                                    i + (" " * (word_space +
                                                                (max(max_len_list[loop_count][i]) - len(i)))) + chars["bottom-right"]) - 1)

        if not i == header_list[-1]:
            header_bottom_line += chars["mid-mid"]
            header_top_line += chars["top-mid"]
            table_bottom_line += chars["bottom-mid"]

        else:
            header_bottom_line += chars["right-mid"]
            header_top_line += chars["top-right"]
            table_bottom_line += chars["bottom-right"]

        loop_count += 1

    loop_count = 0
    for x in range(len(row_list[0])):
        rows.append({str(x): []})
        for i in row_list:
            rows[x][str(x)].append(i[x])

    for x in rows:
        loop_start = True
        for i in rows[sec_loop_count][str(sec_loop_count)]:
            temp_table_row = i
            if loop_start:
                table_row += chars["left"]

            for conf in config:
                sec_text = markup(temp_table_row, conf)
                temp_table_row = sec_text

            table_row += (" " * word_space) + \
                temp_table_row + (" " * (word_space +
                                         max(max_len_list[loop_count][header_list[loop_count]]) - len(i))) + chars["right"]
            loop_count += 1
            loop_start = False
            temp_table_row = ""

        loop_count = 0
        sec_loop_count += 1

        if not x == rows[-1]:
            table_row += "\n"

    table = f'{chars["top-left"] + header_top_line}\n{chars["left"] + table_header}\n{chars["left-mid"] + header_bottom_line}\n{table_row}\n{chars["bottom-left"] + table_bottom_line}'
    return table
