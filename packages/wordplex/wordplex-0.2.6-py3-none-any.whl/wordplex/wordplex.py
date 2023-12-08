import string


class WordPlex:
    def __init__(self):
        self.consonants = [
            "b",
            "c",
            "d",
            "f",
            "g",
            "h",
            "j",
            "k",
            "l",
            "m",
            "n",
            "p",
            "q",
            "r",
            "s",
            "t",
            "v",
            "x",
            "z",
            "w",
        ]
        self.vowels = ["a", "e", "i", "y", "o", "u"]
        self.letters = list(string.ascii_lowercase)
        self.numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self._format = "VC"
        self._suffix = ""
        self._prefix = ""
        self.alphabet_symbol = "@"

    def reset(self):
        self.set_suffix("")
        self.set_prefix("")
        self.set_format("VC")

    def set_prefix(self, p):
        self._prefix = p

    def set_suffix(self, s):
        self._suffix = s

    def set_format(self, format):
        if not format:
            return
        self._format = str(format)

    def set_format_by_word(self, word: str):
        if word is None:
            self.set_format("")
            return

        new_format = ""
        for a in word:
            if self.is_positive_integer(a):
                new_format += "#"
            if a.lower() == self.alphabet_symbol:
                new_format += self.alphabet_symbol
            if a.lower() in self.vowels:
                new_format += "V"
            if a.lower() in self.consonants:
                new_format += "C"
        self.set_format(new_format)

    def get_format(self):
        return self._format

    def similar(self, word=None, cb=None):
        self.set_format_by_word(word)
        return self.go(cb)

    def generate(self, format=None, cb=None):
        self.set_format(format)
        return self.go(cb)

    def go(self, cb):
        if self._format == "":
            return []

        pattern = self.get_pattern()
        return self.fill_position(pattern, 0, len(pattern), "", [], cb)

    def get_pattern(self):
        pattern = []
        for letter in self._format:
            if letter == "C":
                pattern.append(self.consonants)
            elif letter == "V":
                pattern.append(self.vowels)
            elif letter == "#":
                pattern.append(self.numbers)
            elif letter == self.alphabet_symbol:
                pattern.append(self.letters)
            else:
                pattern.append([letter])
        return pattern

    def fill_position(self, pattern, position, length, partial, result, cb=None):
        if position == length - 1:
            for character in pattern[position]:
                word = self._prefix + partial + str(character) + self._suffix
                if callable(cb):
                    cb(word)
                else:
                    result.append(word)
        else:
            for character in pattern[position]:
                self.fill_position(
                    pattern, position + 1, length, partial + str(character), result, cb
                )
        return result

    @staticmethod
    def is_positive_integer(n):
        try:
            return int(n) >= 0
        except ValueError:
            return False
