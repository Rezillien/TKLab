#!/usr/bin/python
import AST
from collections import defaultdict
from SymbolTable import SymbolTable

TTYPE = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

# define operations for integers
for op in ('+', '-', '*', '/', '%', '<<', '>>', '|', '&', '^',
           '<', '>', '<=', '>=', '==', '!=', '&&', '||'):
    TTYPE[op]['int']['int'] = 'int'

# define arithmetic operations for floats
for op in ('+', '-', '*', '/'):
    TTYPE[op]['float']['float'] = 'float'
    TTYPE[op]['float']['int'] = 'float'
    TTYPE[op]['int']['float'] = 'float'

# define logical operations on floats
for op in ('<', '>', '<=', '>=', '==', '!=', '&&', '||'):
    TTYPE[op]['float']['float'] = 'int'

TTYPE['+']['string']['string'] = 'string'
TTYPE['*']['string']['int'] = 'string'

# define logical operations for strings
for op in ('<', '>', '<=', '>=', '==', '!='):  # , '&&', '||'
    TTYPE[op]['string']['string'] = 'int'

# define type casts
TTYPE['cast']['int']['float'] = ['float', 'up']
TTYPE['cast']['float']['int'] = ['int', 'down']


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.scope = SymbolTable(None, "global")

    def visit_Node(self, node):
        print("visit_Node")
        pass

    def visit_Const(self, node):
        print("visit_Const")

    def visit_String(self, node):
        # print("visit_String")
        return 'string'

    def visit_Integer(self, node):
        # print("visit_Integer")
        return 'int'

    def visit_Float(self, node):
        # print("visit_Float")
        return 'float'

    def visit_Matrix(self, node):
        # print("visit_Float")
        return 'matrix'

    def visit_Variable(self, node):
        # print("visit_Variable")
        if self.scope.get(node.value) is None:
            print("Error: Undeclared variable '{}': line {}".format(node.value, 0))
            return
        return self.scope.get(node.value)

    def visit_InstructionList(self, node):
        for i in node.instructions:
            self.visit(i)

    def visit_Rows(self, node):
        print("visit_Rows")
        pass

    def visit_Row(self, node):
        print("visit_Row")
        pass

    def visit_BreakInstruction(self, node):
        # print("visit_BreakInstruction")
        pass

    def visit_ContinueInstruction(self, node):
        # print("visit_ContinueInstruction")
        pass

    def visit_ReturnInstruction(self, node):
        # print("visit_ReturnInstruction")
        pass

    def visit_AssignInstruction(self, node):
        # print("visit_AssignInstruction")
        self.visit(node.operation)
        if self.scope.get(node.variable) is None:
            self.scope.put(node.variable, node.operation.type)

    def visit_ElementAssign(self, node):
        print("visit_ElementAssign")
        pass

    def visit_Zeros(self, node):
        print("visit_Zeros")
        pass

    def visit_Ones(self, node):
        print("visit_Ones")
        pass

    def visit_Eye(self, node):
        print("visit_Eye")
        pass

    def visit_ForInstruction(self, node):
        # print("visit_ForInstruction")
        self.scope = self.scope.pushScope("for")
        self.visit(node.iterator)
        self.visit(node.instruction)
        self.scope = self.scope.getParentScope()

    def visit_WhileInstruction(self, node):
        # print("visit_WhileInstruction")
        self.scope = self.scope.pushScope("while")
        self.visit(node.boolExpr)
        self.visit(node.instruction)
        self.scope = self.scope.getParentScope()
        pass

    def visit_IfInstruction(self, node):
        # print("visit_IfInstruction")
        self.scope = self.scope.pushScope("if")

        self.visit(node.boolExpr)
        self.visit(node.instruction)
        self.scope = self.scope.getParentScope()

        pass

    def visit_IfElseInstruction(self, node):
        # print("visit_IfElseInstruction")
        self.scope = self.scope.pushScope("if")
        self.visit(node.boolExpr)
        self.visit(node.instruction)
        self.visit(node.elseInstruction)
        self.scope = self.scope.getParentScope()
        pass

    def visit_PrintInstruction(self, node):
        # print("visit_PrintInstruction")
        self.visit(node.operation1)
        # print(type(node.operation1))
        if node.twoOperations:
            # print(type(node.operation2))
            self.visit(node.operation2)
        pass

    def visit_GroupedExpression(self, node):
        # print("visit_GroupedExpression")
        self.visit(node.operation)
        pass

    def visit_BinExpression(self, node):
        self.visit(node.left)
        self.visit(node.right)
        node.type = TTYPE[node.operant][node.left.type][node.right.type]
        # print("visit_BinExpression")
        pass

    def visit_CompoundInstruction(self, node):
        # print("visit_CompoundInstruction")
        if node.instructions:
            self.visit(node.instructions)
        pass

    def visit_Iterator(self, node):
        # print("visit_Iterator")
        iteratorType = self.visit(node.iterator)
        if self.scope.get(node.variable) is not None:
            print("Error: Variable already in use '{}': line {}".format(node.variable, 0))
        self.scope.put(node.variable, iteratorType)
        limitType = self.visit(node.list)
        if iteratorType != 'int' or limitType != 'int':
            print("Error: Invalid iterator type '{}': line {}".format(iteratorType, 0))
        pass

    def visit_BoolExpression(self, node):
        # print("visit_BoolExpression")
        self.visit(node.operation1)
        self.visit(node.operation2)
        pass

    def visit_AssignOperation(self, node):
        # print("visit_AssignOperation")
        self.visit(node.variable)
        self.visit(node.operation)
        pass

    def visit_UnaryMinus(self, node):
        print("visit_UnaryMinus")


    def visit_MatrixTransposition(self, node):
        print("visit_MatrixTransposition")


    def visit_Instruction(self, node):
        # print("visit_Instruction")

        self.visit(node.instruction)
        pass
