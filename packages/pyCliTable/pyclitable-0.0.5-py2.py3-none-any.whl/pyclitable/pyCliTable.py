from style import Color

color = Color()


def markup(arg, markup="", table_color=""):
    if markup.lower() == "blue" or table_color.lower() == "blue":
        return color.Blue(arg)
    if markup.lower() == "red" or table_color.lower() == "red":
        return color.Red(arg)
    if markup.lower() == "green" or table_color.lower() == "green":
        return color.Green(arg)
    if markup.lower() == "yellow" or table_color.lower() == "yellow":
        return color.Yellow(arg)
    if markup.lower() == "magenta" or table_color.lower() == "magenta":
        return color.Magenta(arg)
    if markup.lower() == "cyan" or table_color.lower() == "cyan":
        return color.Cyan(arg)
    if markup.lower() == "white" or table_color.lower() == "white":
        return color.White(arg)
    if markup.lower() == "gray" or table_color.lower() == "gray":
        return color.Gray(arg)
    if markup.lower() == "underline" or table_color.lower() == "underline":
        return color.Underline(arg)
    if markup.lower() == "bold" or table_color.lower() == "bold":
        return color.Bold(arg)
    if markup.lower() == "italic" or table_color.lower() == "italic":
        return color.Italic(arg)


def table(data, config='', header_config='', table_color="gray", word_space=2):
    """ data = [
            {"Name": ["Foo", "Fooo", "Fooooo"]},
            {"Surname": ["Bar", "Baar", "Baaar"]},
            {"Gender": ["Male", "Female", "Male"]
        }

    config = ["red", "green", "yellow", "blue", "magenta", "cyan", "gray", "white", "underline", "bold", "italy"]
    header_config = ["red", "green", "yellow", "blue", "magenta", "cyan", "gray", "white", "underline", "bold", "italy"]
    table_color = "red" | "green" | "yellow" | "blue" | "magenta" | "cyan" | "gray" | "white" | "underline" | "bold" | "italy"
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
                                     (max(max_len_list[loop_count][i]) - len(i)))) + markup(chars["right"], table_color=table_color)
        temp_table_row = ""

        header_top_line += chars["top"] * (len((" " * word_space) +
                                               i + (" " * (word_space +
                                                    (max(max_len_list[loop_count][i]) - len(i)))) + chars["top-right"]) - 1)

        header_bottom_line += chars["bottom"] * (len((" " * word_space) +
                                                     i + (" " * (word_space +
                                                          (max(max_len_list[loop_count][i]) - len(i)))) + chars["right"]) - 1)
        lines = chars["bottom"] * (len((" " * word_space) +
                                       i + (" " * (word_space +
                                                   (max(max_len_list[loop_count][i]) - len(i)))) + chars["bottom-right"]) - 1)
        table_bottom_line += markup(lines,
                                    markup="", table_color=table_color)

        if not i == header_list[-1]:
            header_bottom_line += chars["mid-mid"]
            header_top_line += chars["top-mid"]
            table_bottom_line += markup(chars["bottom-mid"],
                                        markup="", table_color=table_color)

        else:
            header_bottom_line += chars["right-mid"]
            header_top_line += chars["top-right"]
            table_bottom_line += markup(chars["bottom-right"],
                                        markup="", table_color=table_color)

        loop_count += 1

    loop_count = 0
    for x in range(len(row_list[0])):
        rows.append({str(x): []})
        for i in row_list:
            try:
                rows[x][str(x)].append(i[x])
            except IndexError:
                rows, x, rows[x][str(x)].append("*****")
                continue

    for x in rows:
        loop_start = True
        for i in rows[sec_loop_count][str(sec_loop_count)]:
            temp_table_row = i
            if loop_start:
                table_row += markup(chars["left"],
                                    markup="", table_color=table_color)

            for conf in config:
                sec_text = markup(temp_table_row, conf)
                temp_table_row = sec_text

            table_row += (" " * word_space) + \
                temp_table_row + (" " * (word_space +
                                         max(max_len_list[loop_count][header_list[loop_count]]) - len(i))) + markup(chars["right"], markup="", table_color=table_color)
            loop_count += 1
            loop_start = False
            temp_table_row = ""

        loop_count = 0
        sec_loop_count += 1

        if not x == rows[-1]:
            table_row += "\n"
            table_row += markup(
                f'{chars["left-mid"] + header_bottom_line}',  table_color=table_color)
            table_row += "\n"

    table = f'{markup(chars["top-left"] + header_top_line, table_color=table_color)}\n{markup(chars["left"], table_color=table_color) + table_header}\n{markup(chars["left-mid"] + header_bottom_line, table_color=table_color)}\n{table_row}\n{markup(chars["bottom-left"], table_color=table_color) + table_bottom_line}'
    return table
