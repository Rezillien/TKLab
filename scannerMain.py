
# !/bin/python
import sys
import ply.lex as lex
from scanner import Scanner


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/scannerexample"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    scanner = Scanner()
    lexer = scanner.lexer
    lexer.input(text)# Give the lexer some input

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break    # No more input
        column = scanner.find_column(tok)
        print("(%d,%d): %s(%s)" %(tok.lineno, column, tok.type, tok.value))
