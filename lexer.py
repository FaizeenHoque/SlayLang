from tokens import *


class Token():
    """
    Represents a single lexical token produced by the Lexer.

    Attributes:
        type (str): The token type, drawn from TokenType.
        value (any): The literal value of the token (e.g. 42, "hello", '+').
    """

    def __init__(self, type: str, value: any):
        """
        Initialize a Token with a type and a value.

        Args:
            type (str): The token type (a TokenType constant).
            value (any): The raw value extracted from the source text.
        """
        self.type = type
        self.value = value

    def __repr__(self):
        """
        Return an unambiguous string representation of the token.

        Returns:
            str: A string in the form 'Token(<type>, <value>)'.
        """
        return f"{self.__class__.__name__}({self.type}, {self.value!r})"


class Lexer:
    """
    Converts a raw source string into a flat list of Token objects.

    The Lexer walks the source character by character, recognising
    whitespace, newlines, string literals, numeric literals, keywords,
    identifiers, built-in function names, operators, punctuation, and
    single-line comments.

    Attributes:
        source (str): The original source code string.
        index (int): The current read position in the source.
        current_character (str | None): The character at the current index,
            or None when the end of the source has been reached.
    """

    def __init__(self, source: str):
        """
        Initialize the Lexer with a source string.

        Args:
            source (str): The source code to lex. Must be non-empty.

        Raises:
            Exception: If source is an empty string.
        """
        self.source = source

        if self.source == '':
            raise Exception("bestie.. you gave nothing to lex 💀")

        self.index = 0
        self.current_character = self.source[self.index]

    def advance(self):
        """
        Move to the next character in the source.

        Increments the index and updates current_character. Sets
        current_character to None when the end of the source is reached.
        """
        self.index += 1
        if self.index >= len(self.source):
            self.current_character = None
        else:
            self.current_character = self.source[self.index]

    def tokenize(self):
        """
        Lex the entire source string and return a list of tokens.

        Iterates over the source, dispatching to specialised read helpers
        based on the current character. Skips spaces and single-line
        comments (//) in place. Appends a final EOF token once the source
        is exhausted.

        Returns:
            list[Token]: All tokens found in the source, terminated by a
            Token of type TokenType.EOF.

        Raises:
            Exception: If an unrecognised character is encountered.
            Exception: If '/' appears without a following '/' (division is
                not yet implemented).
        """
        tokens = []

        while self.current_character is not None:
            if self.current_character == ' ':
                self.advance()

            elif self.current_character == '\n':
                tokens.append(Token(TokenType.NEWLINE, '\n'))
                self.advance()

            elif self.current_character == '"' or self.current_character == "'":
                opening_quote = self.current_character  
                self.advance()
                tokens.append(self.read_string(opening_quote))

            elif self.current_character.isdigit():
                tokens.append(self.read_number())

            elif self.current_character.isalpha() or self.current_character == "_":
                tokens.append(self.read_word())

            elif self.current_character == "/":
                if self.peek() == "/":
                    self.skip_comment()
                else:
                    tokens.append(self.read_operator())

            elif (self.current_character in OPERATORS or (self.peek() is not None and (self.current_character + self.peek()) in OPERATORS)):
                tokens.append(self.read_operator()) 

            elif self.current_character in PUNCTUATION:
                tokens.append(Token(PUNCTUATION.get(self.current_character), self.current_character))
                self.advance()

            else:
                raise Exception(f"bestie... '{self.current_character}' is not valid 💀")

        tokens.append(Token(TokenType.EOF, None))
        return tokens

    def read_string(self, opening_quote):
        """
        Read a string literal, consuming characters until the closing quote.

        Should be called after the opening quote has already been consumed.
        Advances past the closing quote before returning.

        Args:
            opening_quote (str): The quote character that opened the string
                (either '"' or "'"), used to detect the closing delimiter.

        Returns:
            Token: A token of type TokenType.STRING whose value is the
            string contents (excluding the surrounding quotes).

        Raises:
            Exception: If the end of the source is reached before the
                closing quote is found (unterminated string).
        """
        output = ""

        while self.current_character != opening_quote:
            if self.current_character is None:
                raise Exception("unterminated string")

            output += self.current_character
            self.advance()

        self.advance()  # consume closing quote
        return Token(TokenType.STRING, output)

    def read_number(self):
        """
        Read a numeric literal (integer or float) from the source.

        Consumes consecutive digit characters and at most one decimal
        point. Stops at the first character that cannot be part of a
        number (including a second '.').

        Returns:
            Token: A token of type TokenType.NUMBER whose value is either
            an int (if no decimal point was found) or a float.
        """
        number_value = ""
        dot_count = 0

        while self.current_character is not None:
            if self.current_character.isdigit():
                number_value += self.current_character

            elif self.current_character == ".":
                dot_count += 1
                if dot_count > 1:
                    break
                number_value += self.current_character

            else:
                break

            self.advance()

        if "." in number_value:
            return Token(TokenType.NUMBER, float(number_value))
        else:
            return Token(TokenType.NUMBER, int(number_value))

    def read_word(self):
        """
        Read an alphanumeric word and classify it as a keyword, built-in,
        operator alias, or plain identifier.

        Consumes characters while they are alphanumeric or underscores,
        then looks the resulting string up in the KEYWORDS, BUILTINS, and
        OPERATORS tables in that order. Falls back to TokenType.IDENT if
        no match is found.

        Returns:
            Token: A token whose type reflects the classification above and
            whose value is the raw word string.
        """
        word_value = ""

        while self.current_character is not None and (
            self.current_character.isalnum() or self.current_character == "_"
        ):
            word_value += self.current_character
            self.advance()

        if word_value in KEYWORDS:
            token_type = KEYWORDS[word_value]
        elif word_value in BUILTINS:
            token_type = BUILTINS[word_value]
        elif word_value in OPERATORS:
            token_type = OPERATORS[word_value]
        else:
            token_type = TokenType.IDENT

        return Token(token_type, word_value)

    def skip_comment(self):
        """
        Skip a single-line comment, consuming everything up to the newline.

        Expects the current character to be the first '/' of a '//' comment
        marker. Advances past both slashes and then consumes all remaining
        characters on the line, including the terminating newline if present.
        """
        self.advance()  # consume first '/'

        if self.current_character == "/":
            self.advance()  # consume second '/'

            while self.current_character is not None and self.current_character != "\n":
                self.advance()

            if self.current_character == "\n":
                self.advance()  # consume the newline

    def read_operator(self):
        """
        Read a one- or two-character operator from the source.

        First checks whether the current character combined with the next
        forms a recognised two-character operator (e.g. '**', '==', '!=').
        Falls back to a single-character lookup if not. Advances past all
        consumed characters before returning.

        Returns:
            Token: A token whose type is the matching OPERATORS entry and
            whose value is the operator string.

        Raises:
            Exception: If neither the two-character nor single-character
                combination maps to a known operator.
        """
        current = self.current_character
        next_char = self.peek()

        if next_char is not None and (current + next_char) in OPERATORS:
            op = current + next_char
            self.advance()
            self.advance()
            return Token(OPERATORS[op], op)
        
        if current in OPERATORS:
            op = current
            self.advance()
            return Token(OPERATORS[op], op)
        
        raise Exception(f"dawg.. what operator is {current}??")

    def peek(self):
        """
        Look at the next character without consuming it.

        Returns:
            str | None: The character immediately after the current index,
            or None if the current character is the last in the source.
        """
        if self.index + 1 >= len(self.source):
            return None
        return self.source[self.index + 1]


if __name__ == "__main__":
    lexer = Lexer("vibe x = 123 + 45.6 // comment\nyap(x)")
    tokens = lexer.tokenize()
    print(tokens)