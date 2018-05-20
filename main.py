
import sys
import scanner
from Mparser import Mparser
import ply.yacc as yacc

from TreePrinter import TreePrinter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)
    # Tokenize
    # scanner = scanner
    # text = file.read()
    # lexer = scanner.lexer
    # lexer.input(text)  # Give the lexer some input
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break  # No more input
    #     column = scanner.find_column(tok)
    #     print("(%d): %s(%s)" % (tok.lineno, tok.type, tok.value))
    # parser = Mparser.parser/
    # text = file.read()
    # parser.parse(text, lexer=scanner.lexer)

    TreePrinter()
    Mparser = Mparser()
    parser = yacc.yacc(module=Mparser)
    text = file.read()
    program = parser.parse(text, lexer=Mparser.scanner)
    print(program.__str__())
    # print(program.printTree())

