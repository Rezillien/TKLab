
# !/bin/python
import sys
from scanner import Scanner
from MParser import Parser
from ply import yacc

if __name__ == '__main__':

    scanner = Scanner()

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/parserexample"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    m_parser = Parser(debug=False)
    parser = yacc.yacc(module=m_parser)
    ast = parser.parse(text, lexer=m_parser.scanner)
