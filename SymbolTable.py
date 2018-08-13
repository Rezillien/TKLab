
# !/bin/python
class Type:
    pass


class TFloat(Type):
    def __init__(self, value=None):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class TInt(Type):
    def __init__(self, value=None):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class TString(Type):
    def __init__(self, value=None):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class VectorType(Type):
    def __init__(self, value=None, size=0):
        if value is not None:
            size = len(value)
        self.size = size
        self.value = value

    def __str__(self) -> str:
        return "Vector:" + str(self.size)


class MatrixType(Type):
    def __init__(self, value=None, width=0, height=0):
        if value is not None:
            height = len(value)
            width = value[0].size
        self.value = value
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return "Matrix: "+str(self.width) + ";" + str(self.height)


class UndefinedType(Type):
    def __init__(self):
        self.value = None

    def __str__(self) -> str:
        return "UnknownType"


class NoType(Type):
    def __str__(self):
        return "NoType"


class Symbol:
    pass


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type


class SymbolTable:
    def __init__(self):
        self.symbols = []

    def put(self, name, symbol):
        self.symbols[-1][name] = symbol

    def get(self, name):
        for i in range(self.symbols.__len__()-1, -1, -1):
            if name in self.symbols[i]:
                return self.symbols[i][name]
        return None

    def push_scope(self):
        self.symbols.append({})

    def pop_scope(self):
        if self.symbols.__len__() == 0:
            return False
        self.symbols.pop()
        return True


