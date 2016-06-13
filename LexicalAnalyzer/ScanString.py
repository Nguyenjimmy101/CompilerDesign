from LexicalAnalyzer.String import String


def string_scanner(self):
    # save the quote type so we don't stop on a different quote
    quote = self.peek

    string = ''
    while True:
        self._readch()
        if self.peek == '\\':
            # skip escape characters
            string += self.peek
            self._readch()
            string += self.peek
        elif self.peek == quote:
            break
        else:
            string += self.peek

    return String(string)
