#!/usr/bin/env python3
"""Run SlayLang from the command line by wiring the lexer, parser, and evaluator together.

This script checks the file path, loads the source code, and then passes it
through the lexer, parser, and evaluator so a SlayLang file can be executed
from the terminal.
"""

import sys
import os

from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

def main():
    if len(sys.argv) < 2:
        print("usage: slaylang <file.slay>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not filepath.endswith('.slay'):
        print("bestie... that's not a .slay file")
        sys.exit(1)

    if not os.path.exists(filepath):
        print(f"bestie... '{filepath}' doesn't exist")
        sys.exit(1)

    with open(filepath, 'r') as f:
        source = f.read()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator()
        evaluator.evaluate(ast)
    except Exception as e:
        print(f"error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()