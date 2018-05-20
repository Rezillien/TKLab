class Node(object):
    def __str__(self):
        return self.printTree()


class Const(Node):
    def __init__(self, value2, type):
        self.value2 = value2
        self.type = type

    def __str__(self):
        return str(self.value2)


class Integer(Const):
    def __init__(self, value2):
        super().__init__(value2, 'int')

    pass


class Float(Const):
    def __init__(self, value2):
        super().__init__(value2, 'float')


class String(Const):
    def __init__(self, value2):
        super().__init__(value2, 'string')


class Matrix(Const):
    def __init__(self, value2):
        super().__init__(value2, 'matrix')


class Variable(Node):
    def __init__(self, value, ttype=''):
        self.value = value
        self.type = type(value) if ttype == '' else ttype

    def __str__(self):
        return str(self.value)


class InstructionList(Node):
    def __init__(self):
        self.instructions = []

    def addInstruction(self, instr):
        self.instructions.append(instr)


class Rows(Node):
    def __init__(self):
        self.row_list = []

    def append_row(self, a):
        self.row_list.append(a)

    def cons_row(self, row_list, a):
        self.row_list = list(row_list)
        self.row_list.append(a)

    def __str__(self):
        self.printTree()


class Row(Node):
    def __init__(self):
        self.int_list = []

    def append_int(self, a):
        self.int_list.append(a)

    def cons_int(self, int_list, a):
        self.int_list = list(int_list)
        self.int_list.append(a)

    def __str__(self):
        self.printTree()


class AssignInstruction(Node):
    def __init__(self, variable, operation):
        self.variable = variable
        self.operation = operation

    def __str__(self):
        self.printTree()


class ElementAssign(Node):
    def __init__(self, x, y, operation):
        self.x = x
        self.y = y
        self.operation = operation

    def __str__(self):
        self.printTree()


class Zeros(Node):
    def __init__(self, num):
        self.num = num

    def __str__(self):
        self.printTree()


class Ones(Node):
    def __init__(self, num):
        self.num = num

    def __str__(self):
        self.printTree()


class Eye(Node):
    def __init__(self, num):
        self.num = num

    def __str__(self):
        self.printTree()


class BreakInstruction(Node):
    def __init__(self):
        pass

    def __str__(self):
        self.printTree()


class ContinueInstruction(Node):
    def __init__(self):
        pass

    def __str__(self):
        self.printTree()


class ReturnInstruction(Node):
    def __init__(self):
        pass

    def __str__(self):
        self.printTree()


class ForInstruction(Node):
    def __init__(self, iterator, instruction):
        self.iterator = iterator
        self.instruction = instruction

    def __str__(self):
        self.printTree()


class WhileInstruction(Node):
    def __init__(self, boolExpr, instruction):
        self.boolExpr = boolExpr
        self.instruction = instruction

    def __str__(self):
        self.printTree()


class IfInstruction(Node):
    def __init__(self, boolExpr, instruction):
        self.boolExpr = boolExpr
        self.instruction = instruction

    def __str__(self):
        self.printTree()


class IfElseInstruction(Node):
    def __init__(self, boolExpr, instruction, elseInstruction):
        self.boolExpr = boolExpr
        self.instruction = instruction
        self.elseInstruction = elseInstruction

    def __str__(self):
        self.printTree()


class PrintInstruction(Node):
    def __init__(self, operation1, operation2):
        if operation2 is None:
            self.operation1 = operation1
            self.twoOperations = False
        else:
            self.operation1 = operation1
            self.operation2 = operation2
            self.twoOperations = True

    def __str__(self):
        self.printTree()


class GroupedExpression(Node):
    def __init__(self, operation):
        self.operation = operation

    def __str__(self):
        self.printTree()


class BinExpression(Node):
    def __init__(self, operant, left, right):
        self.operant = operant
        self.left = left
        self.right = right
        self.type = ''

    def __str__(self):
        self.printTree()


class CompoundInstruction(Node):
    def __init__(self, instructions):
        self.instructions = instructions

    def __str__(self):
        self.printTree()


class Iterator(Node):
    def __init__(self, variable, iterator, list):
        self.variable = variable
        self.iterator = iterator
        self.list = list

    def __str__(self):
        self.printTree()


class BoolExpression(Node):
    def __init__(self, symbol, operation1, operation2):
        self.symbol = symbol
        self.operation1 = operation1
        self.operation2 = operation2

    def __str__(self):
        self.printTree()


class AssignOperation(Node):
    def __init__(self, assigmentOperation, variable, operation):
        self.assigmentOperation = assigmentOperation
        self.variable = variable
        self.operation = operation

    def __str__(self):
        self.printTree()


class UnaryMinus(Node):
    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        self.printTree()


class MatrixTransposition(Node):
    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        self.printTree()


class Instruction(Node):
    def __init__(self, instruction):
        self.instruction = instruction
