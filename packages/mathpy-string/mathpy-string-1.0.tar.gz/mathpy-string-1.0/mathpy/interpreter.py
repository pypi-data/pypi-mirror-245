from .errors import MathPyNameError, MathPySyntaxError, MathPyTypeError
from .types import (MathPyNull, MathPyBool, MathPyString, MathPyInt, MathPyFloat, MathPyFunction, MathPyList,
                    MathPyNumber)


class MathPySymbolTable:
    def __init__(self, *, parent: "MathPySymbolTable" = None):
        self.parent = parent
        self.table: dict = {}

    def get(self, symbol: str, *, raise_error: bool = True) -> any:
        value = self.table.get(symbol)

        if value is None:
            if self.parent is not None:  # if value not found, search in parent (if it exists)
                return self.parent.get(symbol)

            raise MathPyNameError(f'Name {symbol !r} is not defined')

        return value

    def set(self, symbol: str, new_value: any) -> None:
        if self.get(symbol) is None:
            raise MathPyNameError(f'Name {symbol !r} was not declared in current scope')

        if self.table.get(symbol) is not None:  # check if it's in self first, before parent
            self.table[symbol] = new_value  # symbol defined in self, so change own symbol table

        else:  # self.get() is not None, so parent preset if it's not in self
            self.parent.set(symbol, new_value)  # symbol defined in a parent, so change in parent

    def declare(self, symbol: str, value: any) -> None:
        # even if symbol is declared in parent, declare new local variable
        self.table[symbol] = value if value is not None else MathPyNull()

    def __repr__(self) -> str:
        return f'MathPySymbolTable(parent={self.parent !r})'


class MathPyContext:
    def __init__(self, *, parent: "MathPyContext" = None, top_level: bool = False, display_name: str = None):
        self.parent = parent
        self.display_name = display_name
        self.symbol_table = MathPySymbolTable() if parent is None else MathPySymbolTable(parent=parent.symbol_table)
        self.top_level = top_level

        if top_level is True:
            from .builtin_functions import builtin_functions, bind
            for fnc_name, fnc in builtin_functions.items():
                mathpy_function = MathPyFunction([], "", self, fnc_name)

                bind(mathpy_function, fnc, "call")  # set mathpy.call() to fnc() (need to bind to instance)

                self.declare(fnc_name, mathpy_function)

    def is_top_level(self) -> bool:
        return self.top_level

    def get(self, symbol: str) -> any:
        return self.symbol_table.get(symbol)

    def set(self, symbol: str, new_value: any) -> None:
        return self.symbol_table.set(symbol, new_value)

    def declare(self, symbol: str, value: any) -> None:
        return self.symbol_table.declare(symbol, value)

    def __str__(self) -> str:
        return f"<context at {self.display_name}>" if self.display_name is not None else "<context>"

    def __repr__(self) -> str:
        return f'MathPyContext(display_name={self.display_name !r}, parent={self.parent !r})'


class RuntimeResult:
    def __init__(self, value: any = None, *, return_value: any = None):
        self.value = value if value is not None else MathPyNull()
        self.return_value = return_value

    def get_value(self) -> any:
        return self.value

    def get_return(self) -> any:
        return self.return_value

    def __repr__(self) -> str:
        return f'RuntimeResult({self.value !r}, {self.return_value !r})'


class MathPyInterpreter:
    def __init__(self):
        self.context = MathPyContext(top_level=True, display_name="'main'")

    def interpret(self, ast):
        return self.visit(ast, self.context).get_value()

    def visit(self, node, context: MathPyContext) -> RuntimeResult:
        node_name = node.__class__.__name__  # get node class name in 'str'
        method = getattr(self, f"visit_{node_name}", self.visit_error)
        return method(node, context)

    @staticmethod
    def visit_StringNode(node, context: MathPyContext) -> RuntimeResult:
        value = MathPyString(node.get_value())
        return RuntimeResult(value)

    @staticmethod
    def visit_NumberNode(node, context: MathPyContext) -> RuntimeResult:
        raw_number: str = node.get_value()
        if '.' in raw_number:
            value = MathPyFloat(float(raw_number))
        else:
            value = MathPyInt(int(raw_number))

        return RuntimeResult(value)

    @staticmethod
    def visit_NullTypeNode(node, context: MathPyContext) -> RuntimeResult:
        value = MathPyNull()
        return RuntimeResult(value)

    @staticmethod
    def visit_BooleanNode(node, context: MathPyContext) -> RuntimeResult:
        value = MathPyBool(node.get_value())
        return RuntimeResult(value)

    def visit_VariableDefineNode(self, node, context: MathPyContext) -> RuntimeResult:
        variable_name: str = node.get_name()
        variable_value: any = node.get_value()
        if variable_value is not None:
            variable_value = self.visit(variable_value, context).get_value()  # visit node if it's not None

        context.declare(variable_name, variable_value)
        return RuntimeResult()

    def visit_VariableAssignNode(self, node, context: MathPyContext) -> RuntimeResult:
        variable_name: str = node.get_name()
        variable_value: any = self.visit(node.get_value(), context).get_value()

        context.set(variable_name, variable_value)
        return RuntimeResult()

    @staticmethod
    def visit_VariableAccessNode(node, context: MathPyContext) -> RuntimeResult:  # NOQA
        variable_name: str = node.get_name()
        value = context.get(variable_name)
        return RuntimeResult(value)

    def visit_BinaryOperationNode(self, node, context: MathPyContext) -> RuntimeResult:
        left_value, operator, right_value = node.get_value()
        left_value = self.visit(left_value, context).get_value()  # is Parser Node, turn to Custom Type
        operator = operator.get_value()  # operator is Token, get 'str' value
        right_value = self.visit(right_value, context).get_value()  # is Parser Node, turn to Custom Type

        if operator in ("&&", "||"):
            operator = operator[0]

        value = eval(f"left_value {operator} right_value")  # return MathPyString(x) + MathPyInt(y) for instance
        return RuntimeResult(value)

    def visit_MultipleStatementsNode(self, node, context: MathPyContext) -> RuntimeResult:
        for value in node.get_value():
            current_output: RuntimeResult = self.visit(value, context)  # if not a return, keep visiting node

            if current_output.get_return() is not None:
                if context.is_top_level():  # returns are illegal at top level
                    raise MathPySyntaxError("Illegal 'return' statement at top level", default_message_format=False)

                return current_output  # if not at top level, return the return RuntimeResult

        return RuntimeResult()

    def visit_CodeBlockNode(self, node, context: MathPyContext) -> RuntimeResult:
        code_block_context = MathPyContext(
            parent=context, display_name=f'code block in {context.display_name !r}', top_level=context.top_level
        )  # inherit top level of parent (keep main if code block in main) for return statement

        output: RuntimeResult = self.visit(node.get_value(), code_block_context)  # typically a MultipleStatementsNode

        return output  # output is already RuntimeResult

    @staticmethod
    def visit_FunctionDefineNode(node, context: MathPyContext) -> RuntimeResult:
        function = MathPyFunction(node.get_parameter_names(), node.get_body(), context, node.get_name())
        context.declare(node.get_name(), function)

        return RuntimeResult()

    def visit_FunctionCallNode(self, node, context: MathPyContext) -> RuntimeResult:
        function: MathPyFunction = self.visit(node.get_function_atom(), context).get_value()  # get function from atom

        parameter_values = [self.visit(value, context).get_value() for value in node.get_parameter_values()]

        function_output: RuntimeResult = function.call(*parameter_values)
        return RuntimeResult(function_output.get_return())  # convert return value into normal value

    def visit_ReturnNode(self, node, context: MathPyContext) -> RuntimeResult:
        return_value = node.get_value()
        if return_value is None:
            return RuntimeResult()

        return_value = self.visit(return_value, context).get_value()  # get value to turn into return_value
        return RuntimeResult(return_value=return_value)  # value is MathPyNull() but return_value has value

    def visit_AttributeAccessNode(self, node, context: MathPyContext) -> RuntimeResult:
        atom = self.visit(node.get_atom(), context).get_value()
        attribute_name = node.get_attribute_name()

        attribute = getattr(atom, f'attribute_{attribute_name}', None)
        if attribute is None:
            atom.attribute_error(attribute_name)

        return RuntimeResult(attribute())  # attribute is a method without params

    def visit_MethodCallNode(self, node, context: MathPyContext) -> RuntimeResult:
        atom = self.visit(node.get_atom(), context).get_value()
        method_name = node.get_method_name()
        parameter_list = [self.visit(arg, context).get_value() for arg in node.get_parameter_values()]

        method = getattr(atom, f'method_{method_name}', None)
        if method is None:
            atom.method_error(method_name)

        return RuntimeResult(method(*parameter_list))

    def visit_IfConditionNode(self, node, context: MathPyContext) -> RuntimeResult:
        conditions: list = node.get_conditions()
        body_nodes: list = node.get_body_nodes()
        for condition, body_node in zip(conditions, body_nodes):
            if bool(self.visit(condition, context).get_value()) is True:  # check if condition is fulfilled
                output: RuntimeResult = self.visit(body_node, context)  # visit CodeBlockNode --> creates own context
                return output  # if output has return_value, it will propagate

        return RuntimeResult()

    def visit_WhileLoopNode(self, node, context: MathPyContext) -> RuntimeResult:
        condition = node.get_condition()
        body = node.get_body()

        # create local context so that changes to
        # context within code block are saved
        local_context = MathPyContext(parent=context, display_name="while loop")

        while bool(self.visit(condition, local_context)) is True:
            output: RuntimeResult = self.visit(body, local_context)
            if output.get_return() is not None:  # end if return statement
                return output

        return RuntimeResult()

    def visit_ListNode(self, node, context: MathPyContext) -> RuntimeResult:
        value = MathPyList(self.visit(value, context).get_value() for value in node.get_value())
        return RuntimeResult(value)

    def visit_IterableGetNode(self, node, context: MathPyContext) -> RuntimeResult:
        iterable = self.visit(node.get_node(), context).get_value()
        index = self.visit(node.get_index(), context).get_value()

        if not isinstance(index, MathPyInt):  # Check if index is MathPyInt
            raise MathPyTypeError(f'Iterable indices must be integers, not {index.class_name() !r}')

        value = iterable[int(index)]  # get integer value of index from MathPyInt
        return RuntimeResult(value)

    def visit_UnaryNode(self, node, context: MathPyContext) -> RuntimeResult:
        number = self.visit(node.get_atom(), context).get_value()
        sign_str = node.get_sign()

        if not issubclass(number.__class__, MathPyNumber):
            raise MathPyTypeError(f'Can\'t have unary operations on non-numbers (got type {number.class_name() !r})')

        if sign_str == '+':
            value = number
        elif sign_str == '-':
            value = MathPyInt(-1) * number  # get opposite of number
        else:
            raise MathPySyntaxError("+ or -", sign_str)

        return RuntimeResult(value)

    def visit_ForLoopNode(self, node, context: MathPyContext) -> RuntimeResult:
        var_name: str = node.get_var_name()
        iterable = self.visit(node.get_iterable(), context).get_value()
        body = node.get_body()

        local_context = MathPyContext(parent=context, display_name="for loop")
        local_context.declare(var_name, MathPyNull())

        for value in iterable:
            local_context.set(var_name, value)
            output: RuntimeResult = self.visit(body, local_context)
            if output.get_return() is not None:
                return output

        return RuntimeResult()

    def visit_error(self, node, context: MathPyContext):
        raise Exception(f'Unknown node name {node.__class__.__name__ !r}')
