import ast


class FunctionNode:
    def __init__(self, function_name, file_path, line_number):
        self.function_name = function_name
        self.file_path = file_path
        self.line_number = line_number

        self.source_code = FunctionSourceCode.get_function_source_code(file_path, line_number)
        self.parameters = []
        self.focused_calls = []
        self.conditions_for_focused_calls = {}
        self.parameter_conditions = ""
        self.is_vulnerability_reachable = False
        self.extend_calls = []

        self.unique_id = self._generate_unique_id()

    def to_dict(self):

        return {
            'function_name': self.function_name,
            'file_path': self.file_path,
            'line_number': self.line_number,
            'source_code': self.source_code,
            'parameters': self.parameters,
            'focused_calls': self.focused_calls,
            'extend_calls': self.extend_calls,
            'conditions_for_focused_calls': self.conditions_for_focused_calls,
            'parameter_conditions': self.parameter_conditions,
            'is_vulnerability_reachable': self.is_vulnerability_reachable,
            'unique_id': self.unique_id
        }

    @classmethod
    def from_dict(cls, data):

        node = cls(data['function_name'], data['file_path'], data['line_number'])
        node.source_code = data['source_code']
        node.parameters = data['parameters']
        node.focused_calls = data['focused_calls']
        node.extend_calls = data['extend_calls']
        node.conditions_for_focused_calls = data['conditions_for_focused_calls']
        node.parameter_conditions = data['parameter_conditions']
        node.is_vulnerability_reachable = data['is_vulnerability_reachable']
        node.unique_id = data['unique_id']
        return node

    def _generate_unique_id(self):
        return f"{self.file_path}:{self.function_name}:{self.line_number}"

    def add_parameter(self, param_name):

        self.parameters.append(param_name)

    def add_focused_call(self, call_info):

        self.focused_calls.append(call_info)

    def add_extend_calls(self, extend_calls):
        self.extend_calls.append(extend_calls)


    def add_condition_for_focused_call(self, call_line_number, condition):

        if call_line_number not in self.conditions_for_focused_calls:
            self.conditions_for_focused_calls[call_line_number] = []
        self.conditions_for_focused_calls[call_line_number].append(condition)

    def add_parameter_condition(self, conditions):
        self.parameter_conditions = conditions

    def __repr__(self):
        return (f"FunctionNode(function_name={self.function_name}, file_path={self.file_path}, "
                f"line_number={self.line_number}, parameters={self.parameters}, "
                f"focused_calls={self.focused_calls}, "
                f"conditions_for_focused_calls={self.conditions_for_focused_calls}, "
                f"parameter_conditions={self.parameter_conditions})")

    def __eq__(self, other):
        return isinstance(other, FunctionNode) and self.unique_id == other.unique_id

    def __hash__(self):
        return hash(self.unique_id)




class FunctionCallChain(list):
    def __init__(self, chain=None):
        super().__init__()
        self.chain = chain if chain is not None else []

    def add_node(self, node):
        self.chain.append(node)

    def __repr__(self):
        return f"FunctionCallChain(chain={self.chain})"


class FunctionCallGraph:
    def __init__(self):
        self.graph = {}

    def add_call_relationship(self, caller: FunctionNode, callee: FunctionNode):
        if caller not in self.graph:
            self.graph[caller] = set()
        self.graph[caller].add(callee)

    def get_called_functions(self, caller: FunctionNode):
        return self.graph.get(caller, set())

    def __repr__(self):
        return f"FunctionCallGraph(graph={self.graph})"


class FunctionSourceCode:
    @staticmethod
    def get_function_source_code(file_path, line_number):

        with open(file_path, 'r') as file:
            tree = ast.parse(file.read(), filename=file_path)

        for node in ast.walk(tree):
            if (isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef))  and node.lineno == line_number:
                start_line = node.lineno
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    return ''.join(lines[start_line - 1:end_line])
        return None
