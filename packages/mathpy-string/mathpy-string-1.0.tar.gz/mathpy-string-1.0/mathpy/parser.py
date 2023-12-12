from .errors import MathPySyntaxError
from .parser_nodes import (MultipleStatementsNode, BinaryOperationNode, VariableDefineNode, VariableAssignNode,
                           VariableAccessNode, StringNode, NumberNode, CodeBlockNode, NullTypeNode, FunctionDefineNode,
                           FunctionCallNode, ReturnNode, AttributeAccessNode, MethodCallNode, BooleanNode,
                           IfConditionNode, WhileLoopNode, ListNode, IterableGetNode, UnaryNode, ForLoopNode)


class MathPyParser:
    def __init__(self, token_list: list):
        self.token_list = token_list
        self.current_token = None
        self.current_index = -1

        self.advance()

    def advance(self) -> None:
        self.current_index += 1

        if self.current_index >= len(self.token_list):
            self.current_token = None
        else:
            self.current_token = self.token_list[self.current_index]

    def is_valid_index(self, index) -> bool:
        return len(self.token_list) > index

    def auto_insert_newline(self) -> None:
        from .tokens import Token
        self.token_list.insert(self.current_index, Token(';', 'TT_NEWLINE'))
        self.current_token = self.token_list[self.current_index]  # update current token (can't be none)

    @property
    def future_token(self):
        return self.token_list[self.current_index + 1] if self.is_valid_index(self.current_index + 1) else None

    def parse(self) -> MultipleStatementsNode:
        return self.multiple_statements()

    def parse_shell(self):
        return self.statement()

    # ------------------ Language Grammar ------------------ :
    def sub_atom(self):
        token = self.current_token
        if token is None:
            raise MathPySyntaxError('Unexpected end. Maybe you forgot a ";"?')

        if token.tt_type == 'TT_NAME':
            return self.access_variable()

        elif token.tt_type == 'TT_STRING':
            self.advance()
            return StringNode(token)

        elif token.tt_type == 'TT_NUMBER':
            self.advance()
            return NumberNode(token)

        elif token.tt_type == 'TT_NULL':
            self.advance()
            return NullTypeNode()

        elif token.tt_type == 'TT_BOOLEAN':
            self.advance()
            return BooleanNode(token)

        elif token.get_value() in ['+', '-']:  # Unary (-1 or +1 for instance)
            self.advance()
            number = self.atom()
            return UnaryNode(number, token)

        elif token.tt_type == 'TT_LEFT_BRACKET':
            return self.list_construct()

        elif token.tt_type == 'TT_LEFT_PARENTHESIS':
            self.advance()  # skip left parenthesis
            expression = self.expression()
            if self.current_token.tt_type == 'TT_RIGHT_PARENTHESIS':
                self.advance()  # skip right parenthesis
                return expression
            else:
                raise MathPySyntaxError(")", self.current_token)

    def atom(self, sub_atom=None):
        sub_atom = self.sub_atom() if sub_atom is None else sub_atom
        token = self.current_token

        if token.tt_type == 'TT_LEFT_PARENTHESIS':  # left parenthesis after atom has to be a call
            return self.atom(self.call_function(sub_atom))

        elif token.tt_type == 'TT_DOT':  # atom followed by . has to be attribute access
            attribute = self.access_attribute(sub_atom)
            return self.atom(attribute)  # pass attribute as atom (allows chained attributes)

        elif token.tt_type == 'TT_LEFT_BRACKET':  # IterableGetNode
            return self.atom(self.iterable_get(sub_atom))

        return sub_atom

    def factor(self):
        return self._binary_operation(['*', '/', '%'], self.atom)

    def term(self):
        return self._binary_operation(['+', '-'], self.factor)

    def boolean_operation(self):
        return self._binary_operation(['&&', '||'], self.term)

    def comparison_operation(self):
        return self._binary_operation(['==', '<', '<=', '>', '>='], self.boolean_operation)

    def expression(self):
        return self.comparison_operation()

    def lesser_statement(self, *, insert_newline: bool = True):  # intermediary statement (expressions & code blocks)
        if self.current_token.tt_type == 'TT_LEFT_BRACE':
            self.advance()  # skip left brace
            code_block_body = self.multiple_statements()

            if self.current_token.tt_type == 'TT_RIGHT_BRACE':
                self.advance()  # skip right brace
                if insert_newline: self.auto_insert_newline()  # insert newline since end of statement
                return CodeBlockNode(code_block_body)
            else:
                raise MathPySyntaxError('}', self.current_token)

        return self.expression()

    def statement(self):
        token = self.current_token

        if token.tt_type == 'TT_VARIABLE_DEFINE':
            return self.define_variable()

        elif token.tt_type == 'TT_FUNCTION_DEFINE':
            return self.define_function()

        elif token.tt_type == 'TT_RETURN':
            return self.return_statement()

        elif token.tt_type == 'TT_NAME':
            if self.future_token is not None and self.future_token.tt_type == 'TT_EQUALS_SIGN':
                return self.assign_variable()

        elif token.tt_type == 'TT_CONDITIONAL':
            return self.if_condition()

        elif token.tt_type == 'TT_WHILE':
            return self.while_loop()

        elif token.tt_type == 'TT_FOR':
            return self.for_loop()

        return self.lesser_statement()

    def multiple_statements(self) -> MultipleStatementsNode:
        statement_list = []

        if self.current_token.tt_type != 'TT_NEWLINE':
            statement_list.append(self.statement())

        while self.current_token is not None and self.current_token.tt_type == 'TT_NEWLINE':
            while self.current_token is not None and self.current_token.tt_type == 'TT_NEWLINE':
                self.advance()

            if self.current_token is not None and self.current_token.tt_type != 'TT_RIGHT_BRACE':  # code block: "}"
                statement_list.append(self.statement())

        return MultipleStatementsNode(statement_list)

    # ------------------ Implementation ------------------ :

    def _binary_operation(self, operators: list, function) -> BinaryOperationNode:
        left_node = function()  # get node of lower order

        while self.current_token and self.current_token.get_value() in operators:
            operator = self.current_token
            self.advance()

            right_node = function()
            left_node = BinaryOperationNode(left_node, right_node, operator)

        return left_node  # return lower order node or binary operation node

    def define_variable(self) -> VariableDefineNode:
        self.advance()  # skip 'var' token

        if self.current_token.tt_type != 'TT_NAME':
            raise MathPySyntaxError('name', self.current_token)
        name = self.current_token

        self.advance()

        if self.current_token.tt_type != 'TT_EQUALS_SIGN':
            return VariableDefineNode(name)  # declare without value

        else:
            self.advance()  # skip equals sign

            value = self.expression()
            return VariableDefineNode(name, value)  # declare with value

    def assign_variable(self) -> VariableAssignNode:
        name = self.current_token
        self.advance()

        if self.current_token.tt_type != 'TT_EQUALS_SIGN':
            raise MathPySyntaxError("=", self.current_token)
        self.advance()

        value = self.expression()
        if value is None:
            raise MathPySyntaxError("value")

        return VariableAssignNode(name, value)

    def access_variable(self) -> VariableAccessNode:
        if self.current_token.tt_type != 'TT_NAME':
            raise MathPySyntaxError("name", self.current_token)
        name = self.current_token

        self.advance()
        return VariableAccessNode(name)

    def define_function(self) -> FunctionDefineNode:
        if self.current_token.tt_type != "TT_FUNCTION_DEFINE":
            raise MathPySyntaxError("function", self.current_token)
        self.advance()  # skip "function" keyword

        if self.current_token.tt_type != 'TT_NAME':
            raise MathPySyntaxError('name', self.current_token)
        function_name = self.current_token  # store function name
        self.advance()

        if self.current_token.tt_type != 'TT_LEFT_PARENTHESIS':
            raise MathPySyntaxError('(', self.current_token)
        self.advance()  # skip left parenthesis

        parameter_names = []
        while self.current_token.tt_type == 'TT_NAME':
            parameter_names.append(self.current_token)  # add name token to parameter_names
            self.advance()

            if self.current_token.tt_type == 'TT_COMMA':
                self.advance()  # skip comma, next token is either right parenthesis or name

        if self.current_token.tt_type != 'TT_RIGHT_PARENTHESIS':
            raise MathPySyntaxError(')', self.current_token)
        self.advance()  # skip right parenthesis

        body = self.lesser_statement()

        return FunctionDefineNode(function_name, parameter_names, body)

    def call_function(self, function_atom) -> FunctionCallNode:
        if self.current_token.tt_type != 'TT_LEFT_PARENTHESIS':
            raise MathPySyntaxError('(', self.current_token)
        self.advance()  # skip left parenthesis

        if self.current_token.tt_type == 'TT_RIGHT_PARENTHESIS':
            self.advance()
            return FunctionCallNode(function_atom, [])  # call function without parameters

        parameter_values = []
        parameter_values.append(self.expression())  # append current expression to parameters (has to be expression)

        while self.current_token.tt_type == 'TT_COMMA':
            self.advance()

            if self.current_token.tt_type != 'TT_RIGHT_PARENTHESIS':
                parameter_values.append(self.expression())

        if self.current_token.tt_type != 'TT_RIGHT_PARENTHESIS':
            raise MathPySyntaxError(')', self.current_token)
        self.advance()  # skip right parenthesis

        return FunctionCallNode(function_atom, parameter_values)

    def return_statement(self) -> ReturnNode:
        if self.current_token.tt_type != 'TT_RETURN':
            raise MathPySyntaxError('return', self.current_token)
        self.advance()  # skip 'return' keyword

        if self.current_token.tt_type in ('TT_NEWLINE', 'TT_RIGHT_BRACE'):
            return ReturnNode()
        else:
            return ReturnNode(self.expression())

    def access_attribute(self, atom) -> AttributeAccessNode | MethodCallNode:
        if self.current_token.tt_type != 'TT_DOT':
            raise MathPySyntaxError('.', self.current_token)
        self.advance()  # skip dot

        if self.current_token.tt_type != 'TT_NAME':
            raise MathPySyntaxError('name', self.current_token)
        attribute_name = self.current_token
        self.advance()  # skip name

        if self.current_token.tt_type != 'TT_LEFT_PARENTHESIS':
            return AttributeAccessNode(atom, attribute_name)
        else:
            return self.call_method(atom, attribute_name)

    def call_method(self, atom, method_name) -> MethodCallNode:
        if self.current_token.tt_type != 'TT_LEFT_PARENTHESIS':
            raise MathPySyntaxError('(', self.current_token)
        self.advance()

        parameter_values = []

        if self.current_token.tt_type == 'TT_RIGHT_PARENTHESIS':  # no args, call method with empty args
            self.advance()
            return MethodCallNode(atom, method_name, [])

        parameter_values.append(self.expression())

        while self.current_token.tt_type == 'TT_COMMA':
            self.advance()

            if self.current_token.tt_type != 'TT_RIGHT_PARENTHESIS':
                parameter_values.append(self.expression())
            else:
                return MethodCallNode(atom, method_name, parameter_values)

        if self.current_token.tt_type == 'TT_RIGHT_PARENTHESIS':
            self.advance()
            return MethodCallNode(atom, method_name, parameter_values)
        else:
            raise MathPySyntaxError(')', self.current_token)

    def if_condition_block(self) -> tuple:
        if self.current_token.tt_type == 'TT_CONDITIONAL' and self.current_token.get_value() != 'if':
            raise MathPySyntaxError('if', self.current_token)
        self.advance()

        if self.current_token.tt_type != 'TT_LEFT_PARENTHESIS':
            raise MathPySyntaxError('(', self.current_token)
        self.advance()

        condition_expression = self.expression()

        if self.current_token.tt_type != 'TT_RIGHT_PARENTHESIS':
            raise MathPySyntaxError(')', self.current_token)
        self.advance()

        body_code_block = self.lesser_statement(insert_newline=False)

        return condition_expression, body_code_block

    def if_condition(self) -> IfConditionNode:
        first_condition, first_body = self.if_condition_block()

        condition_list: list = [first_condition]
        body_list: list = [first_body]

        while self.current_token is not None and self.current_token.tt_type == 'TT_CONDITIONAL':
            if self.current_token.get_value() != 'else':  # if it's 'if', return node and make new IfConditionNode
                return IfConditionNode(condition_list, body_list)
            self.advance()  # skip 'else' Token

            if self.current_token.get_value() == 'if':
                condition, body_node = self.if_condition_block()
                condition_list.append(condition)
                body_list.append(body_node)

            else:
                condition_list.append(BooleanNode(True))  # else, so this always executes if the code reaches it
                body_list.append(self.lesser_statement())  # don't skip newline

                return IfConditionNode(condition_list, body_list)  # this is "else" statement, so nothing comes after

        self.auto_insert_newline()  # insert newline for next statement
        return IfConditionNode(condition_list, body_list)

    def while_loop(self) -> WhileLoopNode:
        if self.current_token.tt_type != 'TT_WHILE':
            raise MathPySyntaxError('while', self.current_token)
        self.advance()

        if self.current_token.tt_type != 'TT_LEFT_PARENTHESIS':
            raise MathPySyntaxError('(', self.current_token)
        self.advance()

        condition_expression = self.expression()

        if self.current_token.tt_type != 'TT_RIGHT_PARENTHESIS':
            raise MathPySyntaxError(')', self.current_token)
        self.advance()

        body_node = self.lesser_statement()

        return WhileLoopNode(condition_expression, body_node)

    def list_construct(self) -> ListNode:
        if self.current_token.tt_type != 'TT_LEFT_BRACKET':
            raise MathPySyntaxError('[', self.current_token)
        self.advance()

        if self.current_token.tt_type == 'TT_RIGHT_BRACKET':
            self.advance()
            return ListNode([])

        values = [self.expression()]

        while self.current_token and self.current_token.tt_type == 'TT_COMMA':
            self.advance()

            if self.current_token.tt_type == 'TT_RIGHT_BRACKET':
                self.advance()
                return ListNode(values)

            values.append(self.expression())

        if self.current_token.tt_type != 'TT_RIGHT_BRACKET':
            raise MathPySyntaxError(']', self.current_token)
        self.advance()

        return ListNode(values)

    def iterable_get(self, sub_atom) -> IterableGetNode:
        if self.current_token.tt_type != 'TT_LEFT_BRACKET':
            raise MathPySyntaxError('[', self.current_token)
        self.advance()

        if self.current_token.tt_type == 'TT_RIGHT_BRACKET':
            raise MathPySyntaxError('expression', self.current_token)

        index = self.expression()

        if self.current_token.tt_type != 'TT_RIGHT_BRACKET':
            raise MathPySyntaxError(']', self.current_token)
        self.advance()

        return IterableGetNode(sub_atom, index)

    def for_loop(self) -> ForLoopNode:
        if self.current_token.tt_type != 'TT_FOR':
            raise MathPySyntaxError('for', self.current_token)
        self.advance()  # skip for token

        if self.current_token.tt_type != 'TT_LEFT_PARENTHESIS':
            raise MathPySyntaxError('(', self.current_token)
        self.advance()

        if self.current_token.tt_type != 'TT_NAME':
            raise MathPySyntaxError('name', self.current_token)
        variable_name = self.current_token
        self.advance()

        if self.current_token.tt_type != 'TT_IN':
            raise MathPySyntaxError('in', self.current_token)
        self.advance()

        iterable = self.atom()

        if self.current_token.tt_type != 'TT_RIGHT_PARENTHESIS':
            raise MathPySyntaxError('(', self.current_token)
        self.advance()

        body = self.lesser_statement()

        return ForLoopNode(variable_name, iterable, body)



