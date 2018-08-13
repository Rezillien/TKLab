import AST
from Memory import *
from Exceptions import *
from visit import *


ExpressionDictionary = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '.+': lambda x, y: [[x[i][j] + y[i][j] for i in range(len(x))] for j in range(len(x[0]))],
    '.-': lambda x, y: [[x[i][j] - y[i][j] for i in range(len(x))] for j in range(len(x[0]))],
    '.*': lambda x, y: [[x[i][j] * y[i][j] for i in range(len(x))] for j in range(len(x[0]))],
    './': lambda x, y: [[x[i][j] / y[i][j] for i in range(len(x))] for j in range(len(x[0]))],
    'zeros': lambda x: [[0 for i in range(x)] for j in range(x)],
    'ones': lambda x: [[1 for i in range(x)] for j in range(x)],
    'eye': lambda x: [[1 if j == i else 0 for i in range(x)] for j in range(x)],
    '=': lambda x, y: y,
    '+=': lambda x, y: x + y,
    '-=': lambda x, y: x - y,
    '*=': lambda x, y: x * y,
    '/=': lambda x, y: x / y,
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,
    '<': lambda x, y: x < y,
    '<=': lambda x, y: x <= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
}


class Interpreter(object):

    def __init__(self):
        self.memory = Memory()
        self.memory.push_scope()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.ConstValue)
    def visit(self, node):
        return node.value

    @when(AST.ID)
    def visit(self, node):
        return self.memory.get(node.value)

    @when(AST.Program)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.Range)
    def visit(self, node):
        return range(node.start.accept(self), node.end.accept(self) + 1, node.jump.accept(self))

    @when(AST.For)
    def visit(self, node):
        r = None
        self.memory.push_scope()
        for i in node.range.accept(self):
            self.memory.put(node.id.value, i)
            try:
                r = node.body.accept(self)
            except ContinueException as e:
                continue
            except BreakException as e:
                break
            except ReturnValueException as e:
                return e.value
        self.memory.pop_scope()
        return r

    @when(AST.While)
    def visit(self, node):
        r = None
        self.memory.push_scope()
        while node.condition.accept(self):
            try:
                r = node.body.accept(self)
            except ContinueException as e:
                continue
            except BreakException as e:
                break
            except ReturnValueException as e:
                return e.value
        self.memory.pop_scope()
        return r

    @when(AST.If)
    def visit(self, node):
        self.memory.push_scope()
        if node.condition.accept(self):
            node.body.accept(self)
        self.memory.pop_scope()

    @when(AST.IfElse)
    def visit(self, node):
        self.memory.push_scope()
        if node.condition.accept(self):
            node.body.accept(self)
        else:
            node.else_body.accept(self)
        self.memory.pop_scope()

    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()

    @when(AST.Return)
    def visit(self, node):
        raise ReturnValueException(node.result.accept(self))

    @when(AST.Print)
    def visit(self, node):
        for value in node.printable.accept(self):
            print(value, end=' ')
        print('\b')

    @when(AST.Condition)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return ExpressionDictionary[node.operator](r1, r2)

    @when(AST.Assignment)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        self.memory.put(node.left.id.value, ExpressionDictionary[node.operator](r1, r2))

    @when(AST.AssignTo)
    def visit(self, node):
        return self.memory.get(node.id.value)

    @when(AST.Access)
    def visit(self, node):
        m = node.id.accept(self)
        for value in node.specifier.accept(self):
            m = m[value]
        return m

    @when(AST.Expression)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return ExpressionDictionary[node.operator](r1, r2)

    @when(AST.Transposition)
    def visit(self, node):
        return [list(x) for x in zip(*node.value.accept(self))]

    @when(AST.Negation)
    def visit(self, node):
        return -node.value.accept(self)

    @when(AST.Function)
    def visit(self, node):
        return ExpressionDictionary[node.name](node.argument.accept(self))

    @when(AST.Matrix)
    def visit(self, node):
        list = []
        for row in node.rows:
            list.append(row.accept(self))
        return list

    @when(AST.Sequence)
    def visit(self, node):
        list = []
        for value in node.values:
            list.append(value.accept(self))
        return list

    @when(AST.Error)
    def visit(self, node):
        pass
