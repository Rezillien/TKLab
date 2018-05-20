import AST

INDENT_TOKEN = "| "


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Const)
    def printTree(self, indent=0):
        return indent*INDENT_TOKEN + str(self.value2) + "\n"

    @addToClass(AST.InstructionList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.instructions))

    @addToClass(AST.Rows)
    def printTree(self, indent=0):
        return "ROWS ".join(map(lambda x: x.printTree(indent), self.row_list))

    @addToClass(AST.Row)
    def printTree(self, indent=0):
        return "ROW ".join(map(lambda x: x.printTree(indent), self.int_list))

    @addToClass(AST.AssignInstruction)
    def printTree(self, indent=0):
        return indent * INDENT_TOKEN + "=\n" + (indent+1)*INDENT_TOKEN + self.variable + "\n" + self.operation.printTree(indent+1)

    @addToClass(AST.ElementAssign)
    def printTree(self, indent=0):
        return "[" + self.x.printTree(indent) + \
               "][" + self.y.printTree(indent) + \
               "]=" + self.operation.printTree(indent) + ""

    @addToClass(AST.Zeros)
    def printTree(self, indent=0):
        return "ZEROS " + self.num.printTree(indent) + ""

    @addToClass(AST.Ones)
    def printTree(self, indent=0):
        return "ONES " + self.num.printTree(indent) + ""

    @addToClass(AST.Eye)
    def printTree(self, indent=0):
        return "EYE " + self.num.printTree(indent) + ""

    @addToClass(AST.ForInstruction)
    def printTree(self, indent=0):
        return indent * INDENT_TOKEN + "FOR \n" + self.iterator.printTree(indent+1) + "\n" + self.instruction.printTree(indent) + ""

    @addToClass(AST.WhileInstruction)
    def printTree(self, indent=0):
        return "WHILE\n" + self.boolExpr.printTree(indent+1) + "" + self.instruction.printTree(indent) + ""

    @addToClass(AST.IfInstruction)
    def printTree(self, indent=0):
        return indent*INDENT_TOKEN + "IF\n" + self.boolExpr.printTree(indent+1) + "" + self.instruction.printTree(indent+1) + ""

    @addToClass(AST.IfElseInstruction)
    def printTree(self, indent=0):
        return indent * INDENT_TOKEN +"IF\n" + self.boolExpr.printTree(indent+1) + "" + self.instruction.printTree(indent+1) +\
               indent * INDENT_TOKEN + "ELSE\n" + \
               self.elseInstruction.printTree(indent+1) + ""

    @addToClass(AST.PrintInstruction)
    def printTree(self, indent=0):
        res = indent * INDENT_TOKEN + "PRINT\n" + self.operation1.printTree(indent+1) + ""
        if(self.twoOperations == True):
            res = res + "" + self.operation2.printTree(indent+1) + ""
        return res

    @addToClass(AST.GroupedExpression)
    def printTree(self, indent=0):
        return self.operation.printTree(indent+1) + ""

    @addToClass(AST.BinExpression)
    def printTree(self, indent=0):
        return indent * INDENT_TOKEN + self.operant + "\n" + self.left.printTree(indent+1) + "" + self.right.printTree(indent+1) + ""

    @addToClass(AST.CompoundInstruction)
    def printTree(self, indent=0):
        return self.instructions.printTree(indent + 1) + ""

    @addToClass(AST.Iterator)
    def printTree(self, indent=0):
        return indent * INDENT_TOKEN + self.variable + \
               "\n" + indent*INDENT_TOKEN + "RANGE\n" +\
               (indent+1)*INDENT_TOKEN + self.iterator + "\n" +\
               (indent+1)*INDENT_TOKEN + self.list + ""

    @addToClass(AST.BoolExpression)
    def printTree(self, indent=0):
        if self.operation1 == None or self.operation2 == None:
            return indent*INDENT_TOKEN + self.symbol
        else:
            return indent*INDENT_TOKEN + self.symbol + "\n" + self.operation1.printTree(indent+1) + "" + self.operation2.printTree(indent+1)

    @addToClass(AST.AssignOperation)
    def printTree(self, indent=0):
        return self.assigmentOperation + " " + self.variable.printTree(indent) + " " + self.operation.printTree(indent) + ""

    @addToClass(AST.Instruction)
    def printTree(self, indent=0):
        return self.instruction.printTree(indent) + ""











