import os

# System call
os.system("")


class Color():
    def __init__(self):
        self.red = '\033[31m'
        self.green = '\033[32m'
        self.yellow = '\033[33m'
        self.blue = '\033[34m'
        self.magenta = '\033[35m'
        self.cyan = '\033[36m'
        self.white = '\033[37m'
        self.underline = '\033[4m'
        self.bold = '\033[1m'
        self.italic = '\033[3m'
        self.strikethrough = '\033[9m'
        self.redBackground = "\033[41m"
        self.greenBackground = "\033[42m"
        self.yellowBackground = "\033[43m"
        self.blueBackground = "\033[44m"
        self.magentaBackground = "\033[45m"
        self.cyanBackground = "\033[46m"
        self.whiteBackground = "\033[47m"

    def Red(self, arg):
        return self.red + arg + '\033[0m'

    def Green(self, arg):
        return self.green + arg + '\033[0m'

    def Yellow(self, arg):
        return self.yellow + arg + + '\033[0m'

    def Blue(self, arg):
        return self.blue + arg + '\033[0m'

    def Magenta(self, arg):
        return self.magenta + arg + '\033[0m'

    def Cyan(self, arg):
        return self.cyan + arg + '\033[0m'

    def White(self, arg):
        return self.white + arg + '\033[0m'

    def Underline(self, arg):
        return self.underline + arg + '\033[0m'

    def Bold(self, arg):
        return self.bold + arg + '\033[0m'

    def Italic(self, arg):
        return self.italic + arg + '\033[0m'

    def YellowBackground(self, arg):
        return self.yellowBackground + arg + '\033[0m'


# # Text formatting
# print("\033[1mBold Text\033[0m")  # Bold
# print("\033[3mItalic Text\033[0m")  # Italic
# print("\033[4mUnderline Text\033[0m")  # Underline
# print("\033[9mStrikethrough Text\033[0m")  # Strikethrough

# # Text colors
# print("\033[31mRed Text\033[0m")  # Red text
# print("\033[32mGreen Text\033[0m")  # Green text
# print("\033[33mYellow Text\033[0m")  # Yellow text
# print("\033[34mBlue Text\033[0m")  # Blue text
# print("\033[35mMagenta Text\033[0m")  # Magenta text
# print("\033[36mCyan Text\033[0m")  # Cyan text
# print("\033[37mWhite Text\033[0m")  # White text

# # Background colors
# print("\033[41mRed Background\033[0m")  # Red background
# print("\033[42mGreen Background\033[0m")  # Green background
# print("\033[43mYellow Background\033[0m")  # Yellow background
# print("\033[44mBlue Background\033[0m")  # Blue background
# print("\033[45mMagenta Background\033[0m")  # Magenta background
# print("\033[46mCyan Background\033[0m")  # Cyan background
# print("\033[47mWhite Background\033[0m")  # White background

# # Padding with spaces
# text = "Hello"
# padded_text = text.ljust(10)  # Left-aligned padding with spaces
# print(f'[{padded_text}]')  # Prints "[Hello     ]"

# # Padding with a specific character
# text = "World"
# padded_text = text.rjust(10, '_')  # Right-aligned padding with underscores
# print(f'[{padded_text}]')  # Prints "[_____World]"

# # Centered padding
# text = "Python"
# padded_text = text.center(15, '-')  # Center-aligned padding with dashes
# print(f'[{padded_text}]')  # Prints "[----Python----]"
