class NullTypeNode:
    def __repr__(self) -> str:
        return "NullTypeNode()"


class BooleanNode:
    def __init__(self, value):
        if not isinstance(value, bool):
            self.value = value.get_value() == 'true'  # Token, so check if its value is "true"
        else:
            self.value = value

    def get_value(self) -> bool:
        return self.value

    def __repr__(self) -> str:
        return f'BooleanNode({self.value})'


class NumberNode:
    def __init__(self, value_token):
        self.value_token = value_token

    def get_value(self):
        return self.value_token.get_value()

    def __repr__(self) -> str:
        return f'NumberNode({self.value_token !r})'


class StringNode:
    def __init__(self, value_token):
        self.value_token = value_token

    def get_value(self):
        return self.value_token.get_value()

    def __repr__(self) -> str:
        return f'StringNode({self.value_token !r})'


class BinaryOperationNode:
    def __init__(self, left_expression, right_expression, operator):
        self.left_expression = left_expression  # node
        self.right_expression = right_expression  # node
        self.operator = operator  # str

    def get_value(self) -> tuple:
        return self.left_expression, self.operator, self.right_expression

    def __repr__(self) -> str:
        return f'BinaryOperationNode({self.left_expression !r}, {self.right_expression !r}, {self.operator !r})'


class VariableDefineNode:
    def __init__(self, name, value: any = None):
        self.name = name  # name is a Token
        self.value = value  # None or a Node

    def get_name(self) -> str:
        return self.name.get_value()  # get Token's value

    def get_value(self) -> any:
        return self.value  # is either None or a Node

    def __repr__(self) -> str:
        return f'VariableDefineNode({self.name !r}, {self.value !r})'


class VariableAssignNode:
    def __init__(self, name, value: any):
        self.name = name  # name is a Token
        self.value = value  # value is a Node

    def get_name(self):
        return self.name.get_value()  # get Token's value

    def get_value(self):
        return self.value  # value is a Node

    def __repr__(self) -> str:
        return f'VariableAssignNode({self.name !r}, {self.value !r})'


class VariableAccessNode:
    def __init__(self, name: "Token"):
        self.name = name

    def get_name(self):
        return self.name.get_value()

    def __repr__(self) -> str:
        return f'VariableAccessNode({self.name !r})'


class MultipleStatementsNode:
    def __init__(self, statement_list: list):
        self.statement_list = statement_list

    def get_value(self) -> list:
        return self.statement_list

    def __repr__(self) -> str:
        return f'MultipleStatementsNode({self.statement_list !r})'


class CodeBlockNode:
    def __init__(self, block_body):
        self.block_body = block_body  # MultipleStatementsNode

    def get_value(self) -> MultipleStatementsNode:
        return self.block_body

    def __repr__(self) -> str:
        return f'CodeBlockNode({self.block_body !r})'


class FunctionDefineNode:
    def __init__(self, function_name, parameter_names, body):
        self.function_name = function_name  # is of type Token
        self.parameter_names = parameter_names  # is list of Tokens
        self.body = body  # is Node

    def get_body(self):
        return self.body  # Node, to be visited

    def get_name(self):
        return self.function_name.get_value()  # get Token's value

    def get_parameter_names(self) -> list[str]:
        return [token.get_value() for token in self.parameter_names]  # list of names

    def __repr__(self) -> str:
        return f"FunctionDefineNode({self.function_name !r}, {self.body !r})"


class FunctionCallNode:
    def __init__(self, function_atom, parameter_values: list):
        self.function_atom = function_atom  # is atom
        self.parameter_values = parameter_values

    def get_function_atom(self):
        return self.function_atom

    def get_parameter_values(self) -> list:
        return self.parameter_values

    def __repr__(self) -> str:
        return f'FunctionCallNode({self.function_atom !r}, {self.parameter_values !r})'


class ReturnNode:
    def __init__(self, value=None):
        self.value = value  # is Node

    def get_value(self) -> any:
        return self.value

    def __repr__(self) -> str:
        return f'ReturnNode({self.value})'


class AttributeAccessNode:
    def __init__(self, atom, attribute_name):
        self.atom = atom  # Node
        self.attribute_name = attribute_name  # Token

    def get_atom(self):
        return self.atom

    def get_attribute_name(self):
        return self.attribute_name.get_value()

    def __repr__(self) -> str:
        return f'AttributeAccessNode({self.atom !r}, {self.attribute_name !r})'


class MethodCallNode:
    def __init__(self, atom, method_name, parameter_values: list):
        self.atom = atom  # Node
        self.method_name = method_name  # Token
        self.parameter_values = parameter_values  # list of nodes

    def get_atom(self):
        return self.atom

    def get_method_name(self):
        return self.method_name.get_value()

    def get_parameter_values(self):
        return self.parameter_values

    def __repr__(self) -> str:
        return f'MethodCallNode({self.atom !r}, {self.method_name !r}, {self.parameter_values !r})'


class IfConditionNode:
    def __init__(self, conditions: list, body_nodes: list):
        self.conditions = conditions
        self.body_nodes = body_nodes

    def get_conditions(self) -> list:
        return self.conditions

    def get_body_nodes(self) -> list:
        return self.body_nodes

    def __repr__(self) -> str:
        return f'IfConditionNode({self.conditions !r}, {self.body_nodes !r})'


class WhileLoopNode:
    def __init__(self, condition, body):
        self.condition = condition  # Node
        self.body = body  # Node

    def get_condition(self):
        return self.condition

    def get_body(self):
        return self.body

    def __repr__(self) -> str:
        return f'WhileLoop({self.condition !r}, {self.body !r})'


class ListNode:
    def __init__(self, value: list):
        self.value = value

    def get_value(self) -> list:
        return self.value

    def __repr__(self) -> str:
        return f'ListNode({self.value})'


class IterableGetNode:
    def __init__(self, node, index):
        self.node = node  # node
        self.index = index  # also node

    def get_node(self):
        return self.node

    def get_index(self):
        return self.index

    def __repr__(self) -> str:
        return f'IterableGetNode({self.node !r}, {self.index !r})'


class UnaryNode:
    def __init__(self, atom, sign_token):
        self.atom = atom
        self.sign_token = sign_token

    def get_atom(self):
        return self.atom

    def get_sign(self) -> str:
        return self.sign_token.get_value()

    def __repr__(self) -> str:
        return f'UnaryNode({self.atom !r}, {self.sign_token !r})'


class ForLoopNode:
    def __init__(self, var_name, iterable, body):
        self.var_name = var_name  # token
        self.iterable = iterable  # node
        self.body = body  # node

    def get_var_name(self) -> str:
        return self.var_name.get_value()

    def get_iterable(self):
        return self.iterable

    def get_body(self):
        return self.body

    def __repr__(self) -> str:
        return f'ForLoopNode({self.var_name !r}, {self.iterable !r}, {self.body !r})'

