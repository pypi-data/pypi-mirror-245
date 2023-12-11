from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

def get_lexer(file_type):
    try:
        lexer = get_lexer_by_name(file_type)
    except:
        lexer = get_lexer_by_name('text')
    return lexer

class NotepadsSyntax(object):
    def __init__(self, file_type, code: str):
        self.code: str = code
        self.lexer = get_lexer(file_type)
        self.formatter = TerminalFormatter()

    def __repr__(self):
        return highlight(self.code, self.lexer, self.formatter)

    def __str__(self):
        return str(self.__repr__())