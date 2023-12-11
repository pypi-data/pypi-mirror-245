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
        self.gray = '\033[90m'
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

    def Gray(self, arg):
        return self.gray + arg + '\033[0m'

    def Underline(self, arg):
        return self.underline + arg + '\033[0m'

    def Bold(self, arg):
        return self.bold + arg + '\033[0m'

    def Italic(self, arg):
        return self.italic + arg + '\033[0m'

    def YellowBackground(self, arg):
        return self.yellowBackground + arg + '\033[0m'
