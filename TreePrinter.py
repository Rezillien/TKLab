#   
# !/bin/python
from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


def print_with_ident(value, indent):
     print("| "*indent + str(value))


class TreePrinter:

    IndentSymbol = "|   "

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.ID)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + str(self.value))

    @addToClass(AST.ConstValue)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + str(self.value))

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print_with_ident("For", indent)
        self.id.printTree(indent+1)
        self.range.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print_with_ident("While", indent)
        self.condition.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + "if")
        self.condition.printTree(indent + 1)
        print(indent*TreePrinter.IndentSymbol + "then")
        self.body.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print_with_ident("Range", indent)
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)
        self.jump.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + "break")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + "continue")

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + "return")
        self.result.printTree(indent+1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + "print")
        self.printable.printTree(indent+1)

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + self.operator)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.IfElse)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + "if")
        self.condition.printTree(indent + 1)
        print(indent*TreePrinter.IndentSymbol + "then")
        self.body.printTree(indent + 1)
        print(indent*TreePrinter.IndentSymbol + "else")
        self.else_body.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + self.operator)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + "matrix")
        for row in self.rows:
            row.printTree(indent+1)


    @addToClass(AST.AssignTo)
    def printTree(self, indent=0):
        self.id.printTree(indent)

    @addToClass(AST.Access)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + "access")
        self.id.printTree(indent + 1)
        self.specifier.printTree(indent + 1)

    @addToClass(AST.Expression)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + self.operator)
        print_with_ident(self.operator, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + "transposition")
        self.value.printTree(indent + 1)

    @addToClass(AST.Negation)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + "negate")
        self.value.printTree(indent + 1)

    @addToClass(AST.Function)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + self.name)
        self.argument.printTree(indent+1)
    @addToClass(AST.Sequence)
    def printTree(self, indent=0):
        print(indent*TreePrinter.IndentSymbol + "sequence")
        for value in self.values:
            value.printTree(indent + 1)


