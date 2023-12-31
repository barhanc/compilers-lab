class Memory:
    def __init__(self, name):  # memory name
        self.name = name
        self.symbols = {}

    def has_key(self, name):  # variable name
        return name in self.symbols

    def get(self, name):  # gets from memory current value of variable <name>
        return self.symbols[name] if self.has_key(name) else None

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.symbols[name] = value


class MemoryStack:
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        memory = Memory("global") if memory is None else memory
        self.stack = [memory]

    def get(self, name):  # gets from memory stack current value of variable <name>
        for memory in reversed(self.stack):
            if memory.has_key(name):
                return memory.get(name)
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        for memory in reversed(self.stack):
            if memory.has_key(name):
                return memory.put(name, value)
        self.insert(name, value)

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):  # pops the top memory from the stack
        self.stack.pop()
