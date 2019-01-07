# Lexer that produces a sequence of tokens (keywords + ANY).

def install_keywords(parser):
    global keywords
    keywords = parser.terminals

class Token:
    def __init__(self, type, wordno=-1, extra=''):
        self.type = type
        self.extra = extra
        self.wordno = wordno

    def __cmp__(self, o):
        return cmp(self.type, o)
    def __repr__(self):
        return str(self.type)

def scan(line):
    tokens = []
    wordno = 0
    for t in line.lower().split():
        wordno += 1
        if(t in keywords):
            tokens.append(Token(t, wordno))
        else:
            tokens.append(Token('ANY', wordno, t))
    tokens.append(Token('END'))
    print tokens
    return tokens
