"""
Peter Norvig's Lisp Interpreter for Python
"""

import math, operator as op

#Environment
class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms,args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if var in self else self.outer.find(var)

def add_globals(env):
    "Add some Scheme standard procedures to an environment."
    env.update(vars(math)) # sin, sqrt, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.div, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, 
        '=':op.eq, 'not':op.not_,'equal?':op.eq, 'eq?':op.is_, 
        'cons':lambda x,y:[x]+y, 'car':lambda x:x[0], 'cdr':lambda x:x[1:], 
        'length':len, 'append':op.add, 'list':lambda *x:list(x), 
        'list?': lambda x:isinstance(x,list), 'null?':lambda x:x==[], 
        'symbol?':lambda x: isinstance(x, str)
        })
    return env

global_env = add_globals(Env())

#Eval
def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    while True:
        if isinstance(x, str):         # variable reference
            return env.find(x)[x]
        elif not isinstance(x, list):  # constant literal
            return x                
        elif x[0] == 'quote':          # (quote exp)
            (_, exp) = x
            return exp
        elif x[0] == 'if':             # (if test conseq alt)
            (_, test, conseq, alt) = x
            x = (conseq if eval(test, env) else alt)
        elif x[0] == 'set!':           # (set! var exp)
            (_, var, exp) = x
            env.find(var)[var] = eval(exp, env)
        elif x[0] == 'define':         # (define var exp)
            (_, var, exp) = x
            env[var] = eval(exp, env)
        elif x[0] == 'lambda':         # (lambda (var*) exp)
            (_, vars, exp) = x
            return lambda *args: eval(exp, Env(vars, args, env))
        elif x[0] == 'begin':          # (begin exp*)
            for exp in x[1:]:
                val = eval(exp, env)
            x = x[-1]
        else:                          # (proc exp*)
            exps = [eval(exp, env) for exp in x]
            proc = exps.pop(0)
            return proc(*exps)

#Parse
def parse(s):
    "Read a Scheme expression from a string."
    return read_from(tokenize(s))

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return str(token)

def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    return '('+' '.join(map(to_string, exp))+')' if isinstance(exp, list) else str(exp)

def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        val = eval(parse(raw_input(prompt)))
        if val is not None: print to_string(val)


if __name__ == "__main__":
    repl()
