# !/bin/python
import AST
from SymbolTable import SymbolTable, TFloat, TString, TInt, VectorType, UndefinedType, MatrixType, NoType 
 
 
class NodeVisitor(object): 
 
    def visit(self, node): 
        method = 'visit_' + node.__class__.__name__ 
        visitor = getattr(self, method, self.generic_visit) 
        return visitor(node) 
 
    def generic_visit(self, node): 
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
 
 
def checkType(value, typ): 
    return type(value) is typ 
 
 
class TypeChecker(NodeVisitor): 
 
    def __init__(self): 
        self.errors = False 
        self.symbol_table = SymbolTable() 
 
 
    @staticmethod 
    def checkCompType(type1, type2, lineno): 
        if checkType(type1, VectorType) and checkType(type2, VectorType): 
            if type1.size is not None and type2.size is not None and type1.size != type2.size:
                print("different vector sizes: ", lineno) 
                return TInt() 
            else: 
                return TInt() 
        elif checkType(type1, MatrixType) and checkType(type2, MatrixType): 
            if type1.width is not None and type2.width is not None and type1.height is not None and type2.height is not None and ( 
                    type1.width != type2.width or type1.height != type2.height): 
                print("different matrix sizes: ", lineno) 
                return TInt() 
            else: 
                return TInt() 
        elif (checkType(type1, TFloat) or checkType(type1, TInt)) and ( 
                checkType(type2, TFloat) or checkType(type2, TInt)): 
            return TInt() 
        elif checkType(type1, TString) and checkType(type2, TString): 
            return TInt() 
        return None 
 
    @staticmethod 
    def checkMatrixType(type1, type2, lineno): 
        if checkType(type1, VectorType) and checkType(type2, VectorType): 
            if type1.size is None or type2.size is None: 
                return VectorType() 
            elif type1.size != type2.size: 
                print("different vector sizes: ", lineno) 
                return UndefinedType() 
            else: 
                return VectorType(size=type1.size) 
        elif checkType(type1, MatrixType) and checkType(type2, MatrixType): 
            if type1.width is None or type2.width is None or type1.height is None or type2.height is None: 
                return MatrixType() 
            elif type1.width != type2.width or type1.height != type2.height: 
                print("different matrix sizes: ", lineno) 
                return UndefinedType() 
            else: 
                return MatrixType(width=type1.width, height=type1.height) 
        elif checkType(type1, VectorType) and (checkType(type2, TFloat) or checkType(type2, TInt)): 
            if type1.size is not None: 
                return VectorType(size=type1.size) 
            else: 
                return VectorType() 
        elif checkType(type1, MatrixType) and (checkType(type2, TFloat) or checkType(type2, TInt)): 
            if type1.width is None or type2.width is None: 
                return MatrixType() 
            else: 
                return MatrixType(width=type1.width, height=type1.height) 
        print("different sizes: ", lineno) 
        return None 
 
 
    @staticmethod 
    def checkExprType(type1, type2, op, lineno): 
        result = None 
        if checkType(type1, UndefinedType) or checkType(type2, UndefinedType): 
            result = UndefinedType() 
        elif op == '.+' or op == '.-' or op == '.*' or op == './': 
            result = TypeChecker.checkMatrixType(type1, type2, lineno) 
        elif op == "==" or op == "!=" or op == ">=" or op == "<=" or op == ">" or op == "<": 
            result = TypeChecker.checkCompType(type1, type2, lineno) 
        else: 
            result = TypeChecker.checkBasicType(type1, type2, op) 
        if result is None: 
            return UndefinedType() 
        else: 
            return result 
    @staticmethod 
    def checkBasicType(type1, type2, op): 
        if op == '+': 
            if checkType(type1, TInt) and checkType(type2, TInt): 
                if type1.value is not None and type2.value is not None: 
                    return TInt(type1.value + type2.value) 
                else: 
                    return TInt() 
            elif (checkType(type1, TFloat) or checkType(type1, TInt)) and ( 
                    checkType(type2, TFloat) or checkType(type2, TInt)): 
                if type1.value is not None and type2.value is not None: 
                    return TFloat(type1.value + type2.value) 
                else: 
                    return TFloat() 
            elif checkType(type1, TString) and checkType(type2, TString): 
                if type1.value is not None and type2.value is not None: 
                    return TString(type1.value + type2.value) 
                else: 
                    return TString() 
        elif op == '-': 
            if checkType(type1, TInt) and checkType(type2, TInt): 
                if type1.value is not None and type2.value is not None: 
                    return TInt(type1.value - type2.value) 
                else: 
                    return TInt() 
            elif (checkType(type1, TFloat) or checkType(type1, TInt)) and ( 
                    checkType(type2, TFloat) or checkType(type2, TInt)): 
                if type1.value is not None and type2.value is not None: 
                    return TFloat(type1.value - type2.value) 
                else: 
                    return TFloat() 
 
        elif op == '/': 
            if checkType(type1, TInt) and checkType(type2, TInt): 
                if type1.value is not None and type2.value is not None: 
                    return TInt(type1.value / type2.value) 
                else: 
                    return TInt() 
            elif (checkType(type1, TFloat) or checkType(type1, TInt)) and ( 
                    checkType(type2, TFloat) or checkType(type2, TInt)): 
                if type1.value is not None and type2.value is not None: 
                    return TFloat(type1.value / type2.value) 
                else: 
                    return TFloat() 
 
        elif op == '*': 
            if checkType(type1, TInt) and checkType(type2, TInt): 
                if type1.value is not None and type2.value is not None: 
                    return TInt(type1.value * type2.value) 
                else: 
                    return TInt() 
            elif (checkType(type1, TFloat) or checkType(type1, TInt)) and ( 
                    checkType(type2, TFloat) or checkType(type2, TInt)): 
                if type1.value is not None and type2.value is not None: 
                    return TFloat(type1.value * type2.value) 
                else: 
                    return TFloat() 
            elif checkType(type1, TString) and checkType(type2, TString): 
                if type1.value is not None and type2.value is not None: 
                    return TString(type1.value * type2.value) 
                else: 
                    return TString() 
        return None 
 
    def putVariable(self, id, symbol): 
        name = id.value 
        self.symbol_table.put(name, symbol) 
        return symbol 
 
    def visit_ConstValue(self, node): 
        if checkType(node.value, float): 
            return TFloat(node.value) 
        if checkType(node.value, str): 
            return TString(node.value) 
        if checkType(node.value, int): 
            return TInt(node.value) 
        return UndefinedType() 
 
    def visit_Program(self, node): 
        self.symbol_table.push_scope() 
        for instruction in node.instructions: 
            self.visit(instruction) 
        self.symbol_table.pop_scope() 
 
    def visit_Instructions(self, node): 
        self.symbol_table.push_scope() 
        for instruction in node.instructions: 
            self.visit(instruction) 
        self.symbol_table.pop_scope() 
 
    def visit_ID(self, node): 
        id = self.symbol_table.get(node.value) 
        if id is None: 
            print("undefined variable: " + str(node.lineno)) 
            return UndefinedType() 
        else: 
            return self.symbol_table.get(node.value) 
 
    def visit_Range(self, node): 
        type1 = self.visit(node.start) 
        type2 = self.visit(node.jump) 
        self.visit(node.end) 
        return self.checkExprType(type1, type2, '+', node.lineno) 
 
    def visit_While(self, node): 
        self.symbol_table.push_scope() 
        self.visit(node.condition) 
        self.visit(node.body) 
        self.symbol_table.pop_scope() 
        return NoType() 
 
    def visit_For(self, node): 
        self.symbol_table.push_scope() 
        typ = self.visit(node.range) 
        self.putVariable(node.id, typ) 
        self.visit(node.body) 
        self.symbol_table.pop_scope() 
 
    def visit_If(self, node): 
        self.symbol_table.push_scope() 
        self.visit(node.condition) 
        self.visit(node.body) 
        self.symbol_table.pop_scope() 
        return NoType() 
 
    def visit_IfElse(self, node): 
        self.symbol_table.push_scope() 
        self.visit(node.condition) 
        self.visit(node.body) 
        self.symbol_table.pop_scope() 
        self.symbol_table.push_scope() 
        self.visit(node.else_body) 
        self.symbol_table.pop_scope() 
        return NoType() 
 
    def visit_Continue(self, node): 
        return NoType() 
 
    def visit_Break(self, node): 
        return NoType() 
 
    def visit_Return(self, node): 
        return self.visit(node.result) 
 
    def visit_Condition(self, node): 
        type1 = self.visit(node.left) 
        type2 = self.visit(node.right) 
        return self.checkExprType(type1, type2, node.operator, node.lineno) 
 
    def visit_Print(self, node): 
        self.visit(node.printable) 
        return NoType() 
 
    def visit_Assignment(self, node): 
        type1 = self.visit(node.left) 
        type2 = self.visit(node.right) 
        val = None 
        if node.operator == "=": 
            val = type2 
        else: 
            if type1 is None: 
                val = UndefinedType() 
            else: 
                val = self.checkExprType(type1, type2, node.operator[0], node.lineno) 
        if checkType(node.left.id, AST.Access): 
            return val 
        else: 
            return self.putVariable(node.left.id, val) 
 
    def visit_Expression(self, node): 
        type1 = self.visit(node.left) 
        type2 = self.visit(node.right) 
        return self.checkExprType(type1, type2, node.operator, node.lineno) 
 
    def visit_Access(self, node): 
        typ = self.visit(node.id) 
        spec = self.visit(node.specifier) 
        result = None 
        if checkType(typ, UndefinedType): 
            result = None 
        elif checkType(typ, VectorType): 
            if spec.size != 1: 
                print("vector problem: " + str(spec) + " line: " + str(node.lineno)) 
                result = None 
            else: 
                i = spec.value[0].value 
                if not checkType(i, int): 
                    result = None 
                elif i >= typ.size or i < 0: 
                    print("Index out of bound: " + str(node.lineno)) 
                    result = None 
                elif typ.value is not None: 
                    result = typ.value[i] 
                else: 
                    result = None 
        elif checkType(typ, MatrixType): 
            if spec.size != 2: 
                print("matrix problem: " + str(spec) + " line: " + str(node.lineno)) 
                result = None 
            else: 
                i = spec.value[0].value 
                j = spec.value[1].value 
                if not checkType(j, int) or not checkType(j, int): 
                    result = None 
                elif i >= typ.width or j >= typ.height or i < 0 or j < 0: 
                    print("Index out of bound: " + str(node.lineno)) 
                    result = None 
                elif typ.value is not None: 
                    result = typ.value[i].value[j] 
                else: 
                    result = None 
        else: 
            print(str(typ) + "cannot use access: " + str(node.lineno)) 
        if result is None: 
            return UndefinedType() 
        else: 
            return result 
 
    def visit_AssignTo(self, node): 
        if checkType(node.id, AST.Access): 
            return self.visit(node.id) 
        else: 
            name = node.id.value 
            return self.symbol_table.get(name) 
 
    def visit_Transposition(self, node): 
        typ = self.visit(node.value) 
        if checkType(typ, UndefinedType): 
            return UndefinedType() 
        elif checkType(typ, MatrixType): 
            return MatrixType(width=typ.height, height=typ.width) 
        else: 
            print(str(typ) + " can't be transposed: " + str(node.lineno)) 
            return UndefinedType() 
 
    def visit_Negation(self, node): 
        typ = self.visit(node.value) 
        if checkType(typ, TInt) or checkType(typ, TFloat): 
            typ.value = -typ.value 
        elif checkType(typ, TString): 
            return UndefinedType() 
        else: 
            typ.value = UndefinedType() 
        return typ 
 
    def visit_Sequence(self, node): 
        values = [] 
        for val in node.values: 
            values.append(self.visit(val)) 
        return VectorType(values) 
 
    def visit_Function(self, node): 
        typ = self.visit(node.argument) 
        if checkType(typ, TInt): 
            value = typ.value 
            if value is None or value >= 0: 
                return MatrixType(width=typ.value, height=typ.value) 
            else: 
                print("initialization out of bound: " + str(node.lineno) + " value: " + str(value)) 
        if checkType(typ, UndefinedType): 
            return MatrixType() 
        print("Function initialize with wrong parameter, wanted type Int, got {1} at line {0}" 
              .format(node.lineno, typ)) 
        return UndefinedType() 
 
    def visit_Matrix(self, node): 
        values = [] 
        for val in node.rows: 
            values.append(self.visit(val)) 
        size = values[0].size 
        for val in values: 
            if size != val.size: 
                print("different matrix sizes" + str(node.lineno)) 
                return MatrixType() 
        if len(values) == 1: 
            return values[0] 
        else: 
            return MatrixType(values) 
 
    def visit_Error(self, node): 
        pass
