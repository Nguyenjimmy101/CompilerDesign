class Token(object):
    tag = None

    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return "Token: tag is " + self.tag
