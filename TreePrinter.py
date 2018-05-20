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
        return INDENT_TOKEN * indent + str(self.value2) + "\n"

    @addToClass(AST.InstructionList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent+1), self.instructions))

    @addToClass(AST.Rows)
    def printTree(self, indent=0):
        return "ROWS ".join(map(lambda x: x.printTree(indent+1), self.row_list))

    @addToClass(AST.Row)
    def printTree(self, indent=0):
        return "ROW ".join(map(lambda x: x.printTree(indent+1), self.int_list))

    @addToClass(AST.AssignInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.variable + "=\n" + self.operation.printTree(indent)

    @addToClass(AST.ElementAssign)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "[\n" + self.x.printTree(indent) + \
               "\n][\n" + self.y.printTree(indent) + \
               "\n]\t=" + self.operation.printTree(indent) + "\n"

    @addToClass(AST.Zeros)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "ZEROS " + self.num.printTree(indent) + "\n"

    @addToClass(AST.Ones)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "ONES " + self.num.printTree(indent) + "\n"

    @addToClass(AST.Eye)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "EYE " + self.num.printTree(indent) + "\n"

    @addToClass(AST.ForInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "FOR \n" + self.iterator.printTree(indent+1) + ":\n" + self.instruction.printTree(indent+1) + "\n"

    @addToClass(AST.WhileInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "WHILE " + self.boolExpr.printTree(indent) + ":" + self.instruction.printTree(indent) + "\n"

    @addToClass(AST.IfInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "IF " + self.boolExpr.printTree(indent) + ":" + self.instruction.printTree(indent) + "\n"

    @addToClass(AST.IfElseInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "IF " + self.boolExpr.printTree(indent) + ":" + self.instruction.printTree(indent) + "ELSE: " + self.elseInstruction.printTree(indent) + "\n"

    @addToClass(AST.PrintInstruction)
    def printTree(self, indent=0):
        res = INDENT_TOKEN * indent + "PRINT " + self.operation1.printTree(indent) + "\n"
        if(self.twoOperations == True):
            res = res + self.operation2.printTree(indent) + "\n"
        return res

    @addToClass(AST.GroupedExpression)
    def printTree(self, indent=0):
        return self.operation.printTree(indent+1) + "\n"

    @addToClass(AST.BinExpression)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.operant + " " + self.left.printTree(indent) + " " + self.right.printTree(indent) + "\n"

    @addToClass(AST.CompoundInstruction)
    def printTree(self, indent=0):
        return self.instructions.printTree(indent + 1) + "\n"

    @addToClass(AST.Iterator)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.variable + "=" + self.iterator + ":" + self.list + "\n"

    @addToClass(AST.BoolExpression)
    def printTree(self, indent=0):
        if self.operation1 == None or self.operation2 == None:
            return self.symbol
        else:
            return INDENT_TOKEN * indent + self.symbol + " " + self.operation1.printTree(indent) + "\n" + " " + self.operation2.printTree(indent)

    @addToClass(AST.AssignOperation)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.assigmentOperation + " " + self.variable.printTree(indent) + " " + self.operation.printTree(indent) + "\n"

    @addToClass(AST.Instruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.instruction.printTree(indent) + "\n"











