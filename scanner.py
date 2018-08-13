# !/bin/python
import ply.lex as lex


class Scanner:

    reserved = {
        'print': 'PRINT',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'for': 'FOR',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'eye': 'EYE',
        'zeros': 'ZEROS',
        'ones': 'ONES'
    }
    tokens = [
                 'DOT_PLUS',
                 'DOT_MINUS',
                 'DOT_DIV',
                 'DOT_MUL',

                 'EQ',
                 'NEQ',
                 'GEQ',
                 'LEQ',

                 'PLUS_ASSIGN',
                 'MINUS_ASSIGN',
                 'MUL_ASSIGN',
                 'DIV_ASSIGN',

                 'ID',
                 'FLOAT',
                 'INT',
                 'STRING'
             ] + list(reserved.values())
    literals = "+-*/()[]{}:,;'><="

    t_DOT_PLUS = r'\.\+'
    t_DOT_MINUS = r'\.-'
    t_DOT_MUL = r'\.\*'
    t_DOT_DIV = r'\./'
    t_PLUS_ASSIGN = r'\+='
    t_MINUS_ASSIGN = r'-='
    t_MUL_ASSIGN = r'\*='
    t_DIV_ASSIGN = r'/='
    t_EQ = r'=='
    t_NEQ = r'!='
    t_GEQ = r'>='
    t_LEQ = r'<='

    t_ignore = ' \t\r'

    def __init__(self):
        self.lexer = lex.lex(object=self)

    def t_ignore_COMMENT(self, t):
        r'\#.*'

    def t_FLOAT(self, t):
        r'(\d+\.\d*|\.\d+)(e-?\d+)?'
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r'0|([1-9]\d*)'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'"[^"]*"'
        return t

    def t_ID(self, t):
        r'[a-zA-Z_]\w*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
        t.lexer.skip(1)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()

    def find_column(self, token):
        line_start = self.lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
