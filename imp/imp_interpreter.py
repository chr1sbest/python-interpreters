"""
IMP Language Rules

####
Assignment
    x := 1
Conditional
    if x = 1 then
        y := y
    else
        y := 3
    end
While
    while x < 10 do
        x := x + 1
    end
Compound
    x := 1;
    y := 2
###

"""

import sys
import re
import lexer
from imp_combinators import *

RESERVED = 'RESERVED'
INT = 'INT'
ID = 'ID'

token_exprs = [
        (r'[ \\n\\t]+', None),
        (r'#[^\\n]*',   None),
        (r'\:=',    RESERVED),
        (r'\(',     RESERVED),
        (r'\)',     RESERVED),
        (r';',      RESERVED),
        (r'\+',     RESERVED),
        (r'-',      RESERVED),
        (r'\*',     RESERVED),
        (r'/',      RESERVED),
        (r'<=',     RESERVED),
        (r'<',      RESERVED),
        (r'>=',     RESERVED),
        (r'>',      RESERVED),
        (r'=',      RESERVED),
        (r'!=',     RESERVED),
        (r'and',    RESERVED),
        (r'or',     RESERVED),
        (r'not',    RESERVED),
        (r'if',     RESERVED),
        (r'then',   RESERVED),
        (r'else',   RESERVED),
        (r'while',  RESERVED),
        (r'do',     RESERVED),
        (r'end',    RESERVED),
        (r'[0-9]+',      INT),
        (r'[A-Za-z][A-Za-z0-9_]*', ID),
]

def lex(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\\n' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens

def imp_lex(characters):
    return lexer.lex(characters, token_exprs)
