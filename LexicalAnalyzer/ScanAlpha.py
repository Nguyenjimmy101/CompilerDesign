from LexicalAnalyzer.Bool import Bool
from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Token import Token
from LexicalAnalyzer.Word import Word, Words


def alpha_scanner(self):
    # IDENTIFIERS
    identifier = ''
    while True:
        if self.peek.isalnum():
            identifier += self.peek
            self._readch()
        else:
            self.skip()
            break

    if identifier in ('true', 'false'):
        return Bool(identifier)

    try:
        word = getattr(Words, identifier.upper())
        if word:
            return word
    except AttributeError:
        word = Word(identifier, Tag.ID)
        self.reserve(word)

        token = Token(identifier)
        self.peek = ' '

        return token
