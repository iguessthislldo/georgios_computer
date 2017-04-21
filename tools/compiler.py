#!/usr/bin/env python3

import sys
from pathlib import Path
import re

token_patterns = []
number_pattern = r'[-+]?[0-9]+'
token_patterns.append(number_pattern)

keywords = [
    'if',
    'while',
    'output',
] token_patterns.extend(keywords)

id_pattern = r'[A-Za-z_]+'
token_patterns.append(id_pattern)

seperators = [
    ';',
    r'\{',
    r'\}',
    r'\(',
    r'\)',
]
token_patterns.extend(seperators)

operators = [
    r'\>\=',
    r'\<\=',
    r'\>',
    r'\<',
    r'\+',
    r'\-',
    r'\*',
    r'\/',
    r'\&\&',
    r'\|\|',
    r'\&',
    r'\|',
    r'\!\=',
    r'\=',
    r'\!',
    r'\~',
    r'\^',
]
token_patterns.extend(operators)

token_re = re.compile('(' + '|'.join(token_patterns) + ')')

def main(source, verbose):
    tokens = []
    for lineno, line in enumerate(source.read_text().split('\n')[1:]):
        tokens.extend(token_re.findall(line))

    print(tokens)

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('-v', dest='verbose', action='store_true')

    args = parser.parse_args()

    main(args.source, args.verbose)

