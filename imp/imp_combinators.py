class Result(object):
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

    def __repr__(self):
        return 'Result({0}, {1})'.format(self.value, self.pos)


class Parser(object):
    def __call__(self, tokens, pos):
        return None

    def __add__(self, other):
        return Concat(self, other)

    def __mul__(self, other):
        return Exp(self, other)
    
    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, other):
        return Process(self, function)


class Reserved(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and \
                tokens[pos][0] == self.value and \
                tokens[pos][1] is self.tag:
                    return Result(tokens[pos][0], pos + 1)
        return None


class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and \
                tokens[pos][1] is self.tag:
                    return Result(tokens[pos][0], pos + 1)
        return None

class Concat(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            right_result = self.right(tokens, left_result.pos)
            if right_result:
                combined_value = (left_result.value, right_result.value)
                return Result(combined_value, right_result.pos)
        return None

class Alternate(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            return left_result
        else:
            right_result = self.right(tokens, pos)
            return right_result


class Opt(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            return result
        return Result(None, pos)


class Rep(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        results = []
        result = self.parser(tokens, pos)
        while result:
            results.append(result.value)
            pos = result.pos
            result = self.parser(tokens, pos)
        return Result(results, pos)


class Process(Parser):
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            result.value = self.function(result.value)
            return result


class Lazy(Parser):
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser(tokens, pos)


