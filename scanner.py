import ply.lex as lex

tokens = [
    'DOTPLUS', 'DOTMINUS', 'DOTMULTIPLE', 'DOTDIVIDE',
    'EQUAL', 'PLUSEQUAL', 'MINUSEQUAL', 'MULTIPLEEQUAL', 'DIVIDEEQUAL',
    'ISLESS', 'ISMORE', 'ISLESSOREQUAL', 'ISMOREOREQUAL', 'ISNOTEQUAL', 'ISEQUAL',
    'IF', 'ELSE', 'WHILE',
    'BREAK', 'CONTINUE', 'RETURN',
    'EYE', 'ZEROS', 'ONES',
    'PRINT',
    'ID',
    'INT',
    'FLOAT',
    'COMMENT'
]

literals = [
    '+', '-', '*', '/',
    '(', ')', '[', ']', '{', '}',
    ':',
    ',', ';',
    '\'',
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
    r'='
    return t


def t_ISLESS(t):
    r'<'
    return t


def t_ISMORE(t):
    r'>'
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
    r'if'
    return t


def t_ELSE(t):
    r'else'
    return t


def t_WHILE(t):
    r'while'
    return t


def t_BREAK(t):
    r'break'
    return t


def t_CONTINUE(t):
    r'continue'
    return t


def t_RETURN(t):
    r'return'
    return t


def t_ZEROS(t):
    r'zeros'
    return t


def t_ONES(t):
    r'ones'
    return t


def t_PRINT(t):
    r'print'
    return t


def t_EYE(t):
    r'eye'
    return t


def t_ID(t):
    r'[a-zA-Z_]\w*'
    return t


def t_INT(t):
    r'[0-9]+'
    return t


def t_FLOAT(t):
    r'[+-]?([0-9]*[.])?[0-9]+'
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


def find_column(text, tok):
    return None
