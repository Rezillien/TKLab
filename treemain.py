# !/bin/python
import sys
import ply.yacc as yacc
from MParser import Parser
from TreePrinter import TreePrinter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/treeexample"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Mparser = Parser()
    parser = yacc.yacc(module=Mparser)
    text = file.read()
    ast = parser.parse(text, lexer=Mparser.scanner)
    ast.printTree()
