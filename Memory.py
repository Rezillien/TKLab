class Memory:
    def __init__(self):
        self.symbols = []

    def put(self, name, symbol):
        self.symbols[-1][name] = symbol

    def get(self, name):
        for i in range(self.symbols.__len__()-1, -1, -1):
            if name in self.symbols[i]:
                return self.symbols[i][name]
        return None

    def has_key(self, name):
        for i in range(self.symbols.__len__()-1, -1, -1):
            if name in self.symbols[i]:
                return True
        return False

    def push_scope(self):
        self.symbols.append({})

    def pop_scope(self):
        if self.symbols.__len__() == 0:
            return False
        self.symbols.pop()
        return True



