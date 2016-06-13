from LexicalAnalyzer.Num import Num
from LexicalAnalyzer.Real import Real


def number_scanner(self):
    # NUMBERS
    number = 0
    while True:
        if self.peek.isnumeric():
            number = 10 * number + int(self.peek)
            self._readch()
        else:
            break

    if self.peek != '.':
        self.skip()
        return Num(number)

    number = float(number)
    digit = 10

    while True:
        if self.peek.isnumeric():
            number += int(self.peek) / digit
            digit *= 10
            self._readch()
        else:
            break
    return Real(number)
