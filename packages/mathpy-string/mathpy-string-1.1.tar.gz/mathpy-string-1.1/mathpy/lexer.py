from .tokens import Token
from .errors import MathPyIllegalCharError, MathPySyntaxError
from .common import module_folder
import json

with open(f'{module_folder}/language_grammar/token_types.json', 'rt', encoding='utf-8') as token_types_file:
    token_types = json.loads(token_types_file.read())

with open(f'{module_folder}/language_grammar/keywords.json', 'rt', encoding='utf-8') as keywords_file:
    token_keywords: dict = json.loads(keywords_file.read())

token_type_lookup = {}
for tt_type, char_list in token_types.items():
    for composed_char in char_list:
        if tt_type[0] != "_":
            token_type_lookup[composed_char] = tt_type


class MathPyLexer:
    default_treatment_types = token_types['TT_NEWLINE'] + token_types['TT_EQUALS_SIGN']

    def __init__(self, code_text: str):
        self.code_text = code_text
        self.current_char = None
        self.current_index = -1

        self.current_line = 0
        self.current_column = 0

        self.advance()

    def advance(self) -> None:
        if self.current_char == '\n':
            self.current_line += 1
            self.current_column = 0

        self.current_index += 1

        if self.current_index >= len(self.code_text):
            self.current_char = None
        else:
            self.current_column += 1
            self.current_char = self.code_text[self.current_index]

    def make_name(self) -> Token:
        line_start = self.current_line
        column_start = self.current_column

        name = self.current_char
        self.advance()

        while self.current_char in token_types['TT_NAME'] + token_types['_TT_NAME_EXTENSION']:
            name += self.current_char
            self.advance()

        if name in token_keywords.keys():
            return Token(name, token_keywords[name], line_start, column_start)

        return Token(name, 'TT_NAME', line_start, column_start)

    def make_string(self) -> Token:
        line_start = self.current_line
        column_start = self.current_column

        quote = self.current_char
        string_value = ''
        self.advance()

        while self.current_char not in [quote, '\n']:
            string_value += self.current_char
            self.advance()

        if self.current_char == quote:
            self.advance()
        else:
            Exception('Incomplete input')

        return Token(string_value, 'TT_STRING', line_start, column_start)

    def make_number(self) -> Token:
        line_start = self.current_line
        column_start = self.current_column

        number_string = self.current_char
        self.advance()

        has_dot = False
        while self.current_char in token_types['TT_DIGIT'] or (self.current_char in token_types['TT_DOT'] and has_dot is False):
            if self.current_char in token_types['TT_DOT']:
                has_dot = True

            number_string += self.current_char
            self.advance()

        return Token(number_string, 'TT_NUMBER', line_start, column_start)

    def make_comment(self) -> None:
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def make_equals(self) -> Token:
        first_char: str = self.current_char
        tt_type = "TT_EQUALS_SIGN"

        line = self.current_line
        column = self.current_column

        self.advance()

        if first_char + self.current_char in token_types["TT_BOOLEAN_OPERATOR"]:
            first_char = first_char + self.current_char
            tt_type = "TT_BOOLEAN_OPERATOR"
            self.advance()

        return Token(first_char, tt_type, line, column)

    def make_boolean_operator(self) -> Token:
        first_char = self.current_char
        line = self.current_line
        column = self.current_column

        self.advance()

        if first_char + self.current_char in token_types["TT_BOOLEAN_OPERATOR"]:
            token = Token(first_char + self.current_char, "TT_BOOLEAN_OPERATOR", line, column)
            self.advance()
            return token

        if first_char in ('&', '|'):
            raise MathPySyntaxError(f"Invalid boolean operator at line {line}, column {column}")
        else:
            return Token(first_char, 'TT_BOOLEAN_OPERATOR', line, column)

    # -------------------------- Tokenize process --------------------------

    def default_tokenize_treatment(self, token_list: list, token_type: str) -> None:
        token_list.append(Token(self.current_char, token_type, self.current_line, self.current_column))
        self.advance()

    def tokenize(self) -> list[Token]:
        token_list: list = []

        while self.current_char is not None:
            if self.current_char in token_types["TT_IGNORE"]:
                self.advance()

            elif self.current_char in token_types["TT_EQUALS_SIGN"]:
                token_list.append(self.make_equals())

            elif self.current_char in ("&", "|", "<", ">"):
                token_list.append(self.make_boolean_operator())

            elif self.current_char in token_types["TT_QUOTE"]:
                token_list.append(self.make_string())

            elif self.current_char in token_types["TT_NAME"]:
                token_list.append(self.make_name())

            elif self.current_char in token_types["TT_DIGIT"]:
                token_list.append(self.make_number())

            elif self.current_char in token_types["TT_COMMENT"]:
                self.make_comment()  # don't append as this does not create a token

            else:
                current_tt_type = token_type_lookup.get(self.current_char)
                if current_tt_type is not None:
                    self.default_tokenize_treatment(token_list, current_tt_type)
                else:
                    raise MathPyIllegalCharError(f"Illegal character at line {self.current_line}, column {self.current_column}")

        return token_list
