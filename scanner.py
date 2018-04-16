import ply.lex as lex


literals = [
    '+', '-', '*', '/',
    '(', ')', '[', ']', '{', '}',
    ':',
    ',', ';',
    '\'',
    '=', '>', '<',
]
tokens = [
    'DOTPLUS', 'DOTMINUS', 'DOTMULTIPLE', 'DOTDIVIDE',
    'EQUAL', 'PLUSEQUAL', 'MINUSEQUAL', 'MULTIPLEEQUAL', 'DIVIDEEQUAL',
    'ISLESSOREQUAL', 'ISMOREOREQUAL', 'ISNOTEQUAL', 'ISEQUAL',
    'IF', 'ELSE', 'WHILE', 'FOR',
    'BREAK', 'CONTINUE', 'RETURN',
    'EYE', 'ZEROS', 'ONES',
    'PRINT',
    'ID',
    'INT',
    'FLOAT',
    'STRING',
    'COMMENT',
]


def t_DOTPLUS(t):
    r'\.\+'
    return t


def t_DOTMINUS(t):
    r'\.\-'
    return t


def t_DOTMULTIPLE(t):
    r'\.\*'
    return t


def t_DOTDIVIDE(t):
    r'\./'
    return t


def t_PLUSEQUAL(t):
    r'\+='
    return t


def t_MINUSEQUAL(t):
    r'\-='
    return t


def t_MULTIPLEEQUAL(t):
    r'\*='
    return t


def t_DIVIDEEQUAL(t):
    r'/='
    return t


def t_EQUAL(t):
    r'=='
    return t


def t_ISLESSOREQUAL(t):
    r'<='
    return t


def t_ISMOREOREQUAL(t):
    r'>='
    return t


def t_ISNOTEQUAL(t):
    r'!='
    return t


def t_ISEQUAL(t):
    r'=='
    return t


def t_IF(t):
    r'\bif\b'
    return t


def t_ELSE(t):
    r'\belse\b'
    return t


def t_WHILE(t):
    r'\bwhile\b'
    return t

def t_FOR(t):
    r'\bfor\b'
    return t


def t_BREAK(t):
    r'\bbreak\b'
    return t


def t_CONTINUE(t):
    r'\bcontinue\b'
    return t


def t_RETURN(t):
    r'\breturn\b'
    return t


def t_ZEROS(t):
    r'\bzeros\b'
    return t


def t_ONES(t):
    r'\bones\b'
    return t


def t_PRINT(t):
    r'\bprint\b'
    return t


def t_EYE(t):
    r'\beye\b'
    return t

def t_NAMEERROR(t):
    r'[+-]?([0-9]+|([0-9]*[.])?[0-9]+)[a-zA-Z]'
    print("Illegal ID name '%s'" % t.value[0])
    t.lexer.skip(1)

def t_ID(t):
    r'[a-zA-Z_]\w*'
    return t

def t_FLOAT(t):
    r"\d+(\.\d*)|\.\d+"
    return t

def t_INT(t):
    r'\d+'
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t


def t_COMMENT(t):
    r'\#.*'
    pass




t_ignore = '  \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def find_column(token):
    last_cr = lexer.lexdata.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    return token.lexpos - last_cr
