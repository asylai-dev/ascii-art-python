import sys
import shutil


def get_start(char):
    return (ord(char) - 32) * 9
def main():
    if len(sys.argv) < 2:
        sys.exit()

    output_file = None
    color = None
    to_color = None
    align = None

    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m"
    }

    reset = "\033[0m"

    if sys.argv[1].startswith("--reverse="):
        reverse_file = sys.argv[1].split("=", 1)[1]

        with open(reverse_file, "r") as file:
            reverse_data = file.readlines()

        with open("standard.txt", "r") as file:
            banner_data = file.readlines()

        lines = []

        for line in reverse_data:
            lines.append(line.rstrip("\n"))

        text_result = ""
        position = 0

        while position < len(lines[0]):
            found = False

            for code in range(32, 127):
                start = (code - 32) * 9
                symbol_art = []

                for i in range(1, 9):
                    symbol_art.append(banner_data[start + i].rstrip("\n"))

                width = len(symbol_art[0])
                match = True

                for i in range(8):
                    piece = lines[i][position:position + width]

                    if piece != symbol_art[i]:
                        match = False
                        break

                if match:
                    text_result += chr(code)
                    position += width
                    found = True
                    break

            if not found:
                position += 1

        print(text_result)
        sys.exit()

    elif sys.argv[1].startswith("--align="):
        align = sys.argv[1].split("=", 1)[1]
        text = sys.argv[2].replace("\\n", "\n")

        if len(sys.argv) >= 4:
            style = sys.argv[3]
        else:
            style = "standard"

    elif sys.argv[1].startswith("--color="):
        color = sys.argv[1].split("=", 1)[1]

        if color not in colors:
            print("Invalid color")
            sys.exit()

        if len(sys.argv) >= 4:
            to_color = sys.argv[2]
            text = sys.argv[3].replace("\\n", "\n")

            if len(sys.argv) >= 5:
                style = sys.argv[4]
            else:
                style = "standard"

        else:
            text = sys.argv[2].replace("\\n", "\n")
            style = "standard"

    elif sys.argv[1].startswith("--output="):
        output_file = sys.argv[1].split("=", 1)[1]
        text = sys.argv[2].replace("\\n", "\n")
        if len(sys.argv) >= 4:
            style = sys.argv[3]
        else:
            style = "standard"

    else:
        text = sys.argv[1].replace("\\n", "\n")
        if len(sys.argv) >= 3:
            style = sys.argv[2]
        else:
            style = "standard"

    if style not in ["standard", "shadow", "thinkertoy"]:
        print("Invalid style")
        sys.exit()

    if align is not None and align not in ["left","right", "center","justify"]:
        print("Invalid align")
        sys.exit()
    filename = style + ".txt"
    with open(filename, "r") as file:
        data = file.readlines()

    terminal_width = shutil.get_terminal_size().columns

    parts = text.split("\n")
    result = ""

    for part in parts:
        for i in range(1, 9):
            line = ""
            color_start = -1
            color_end = -1

            for index, char in enumerate(part):
                if (to_color is not None and part.startswith(to_color, index)):
                    color_start = index
                    color_end = index + len(to_color)

                start = get_start(char)
                art = data[start + i].rstrip("\n")

                if color and to_color is None:
                    line += colors[color] + art + reset

                elif color and color_start <= index < color_end:
                    line += colors[color] + art + reset

                else:
                    line += art
            if align == "center":
                plain_length = 0
                for char in part:
                    start = get_start(char)
                    plain_length += len(data[start + i].rstrip("\n"))
                spaces = max(0,(terminal_width - plain_length) // 2)
                result += " " * spaces + line + "\n"
            elif align == "right":
                plain_length = 0
                for char in part:
                    start = get_start(char)
                    plain_length += len(
                        data[start + i].rstrip("\n")
                    )
                spaces = max(0,terminal_width - plain_length)
                result += " " * spaces + line + "\n"
            elif align == "justify":
                words = part.split(" ")
                if len(words) <= 1:
                    result += line + "\n"
                else:
                    words_art = []
                    for word in words:
                        word_line = ""
                        for char in word:
                            start = get_start(char)
                            word_line += data[start + i].rstrip("\n")
                        words_art.append(word_line)
                    words_width = 0
                    for word_art in words_art:
                        words_width += len(word_art)
                    gaps = len(words_art) - 1
                    spaces = (terminal_width - words_width ) // gaps
                    extra = (terminal_width - words_width) % gaps
                    for j in range(len(words_art)):
                        result += words_art[j]
                        if j < gaps:
                            result += " " * spaces
                            if extra > 0:
                                result += " "
                                extra -= 1
                    result += "\n"
            else:
                result += line + "\n"
    if output_file:
        with open(output_file, "w") as file:
            file.write(result)
    else:
        print(result, end="")

if __name__ == "__main__":
    main()