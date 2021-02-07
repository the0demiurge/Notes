"""Calculator, worte in AST in python
"""
# This could be implemented as string-based big-number calcaulation
from ast import literal_eval
from math import inf


def ADD(x, y):
    return str(literal_eval(x) + literal_eval(y))


def SUB(x, y):
    return str(literal_eval(x) - literal_eval(y))


def POW(x, y):
    return str(literal_eval(x) ** literal_eval(y))


def MUL(x, y):
    return str(literal_eval(x) * literal_eval(y))


def DIV(x, y):
    return str(literal_eval(x) / literal_eval(y))


operations = {
    # 'op': [priority, function]
    '+': [1, ADD],
    '-': [1, SUB],
    '*': [2, MUL],
    '/': [2, DIV],
    '^': [3, POW]
}
parens = {
    '(': 1,
    ')': -1
}


class TreeNode(object):
    __slots__ = ('val', 'left', 'right')

    def __init__(self, val=None, left=None, right=None):
        self.val, self.left, self.right = val, left, right

    def __repr__(self):
        left, right = ' ', ' '
        if self.left is not None:
            left = repr(self.left) + ' <- '
        if self.right is not None:
            right = ' -> ' + repr(self.right)
        return '(' + left + repr(self.val) + right + ')'


def lexer(string):
    # removing useless parens
    result = list()
    if not string:
        return result
    head, tail = 0, 0  # head and tail are used for slice number out

    numeric = False  # Stores previous scanned atom type. If numeric changes, the successor atom type will change
    while tail < len(string):
        # if '+' '-' are operators
        if string[tail] in {'+', '-'} and numeric:
            numeric = False
            result.append(('SYMB', string[tail]))
        # elif numbers or '+' '-' are numbers' symbol
        elif (string[tail].isdecimal() or string[tail] == '.') or (string[tail] in {'+', '-'} and not numeric):
            numeric = True
            head = tail
            tail += 1
            while tail < len(string) and (string[tail].isdecimal() or string[tail] == '.'):
                tail += 1
            num = string[head:tail]
            if num in {'+', '-'}:
                num += '1'
            result.append(('NUM', num))
            tail -= 1
        # elif operators or parentheses
        elif string[tail] in {'*', '/', '^', '(', ')'}:
            symb = 'PAREN' if string[tail] in parens else 'SYMB'
            if numeric and string[tail] == '(':
                result.append(('SYMB', '*'))
            numeric = True if string[tail] == ')' else False
            result.append((symb, string[tail]))
        tail += 1
    return result


def parser(tokens):
    # Remove useless parens
    remove_enclosing_parans_flag = True
    while remove_enclosing_parans_flag:
        if len(tokens) == 0:
            return
        remove_enclosing_parans_flag = remove_enclosing_parans_flag and (tokens[0][1] == '(' and tokens[-1][1] == ')')
        depth = 0
        for TYPE, TOKEN in tokens[:-1]:
            depth += parens.get(TOKEN, 0)
            if depth == 0:
                remove_enclosing_parans_flag = remove_enclosing_parans_flag and (depth != 0)
                break
        if remove_enclosing_parans_flag:
            tokens = tokens[1:-1]

    depth = 0
    min_priority = inf
    min_priority_index = None

    # find the operator out of parentheses with smallest priority
    for i, (TYPE, TOKEN) in enumerate(tokens):
        # judge weather in parentheses or not
        if TYPE == 'PAREN':
            depth += parens[TOKEN]

        elif TYPE == 'SYMB' and depth == 0:
            if operations[TOKEN][0] < min_priority:
                min_priority_index, min_priority = i, operations[TOKEN][0]

    if min_priority_index is None:
        if tokens[0][1] in parens or tokens[0][1] in operations:
            return
        else:
            return TreeNode(tokens[0][1])

    left = parser(tokens[:min_priority_index])
    right = parser(tokens[min_priority_index + 1:])
    return TreeNode(tokens[min_priority_index][1], left, right)


def solve(ast_root, DEBUG=False):
    """Traverse the AST and do calculation
    """
    if ast_root is None:
        raise ValueError('AST cannot be None')
    if ast_root.left is ast_root.right is None:
        return ast_root.val
    else:
        if DEBUG:
            left = solve(ast_root.left, DEBUG)
            right = solve(ast_root.right, DEBUG)
            result = operations[ast_root.val][1](left, right)
            print('Calculating:', ast_root.val, ast_root.left, '|', ast_root.right, '=>', left, ast_root.val, right, '=', result)
            return result
        else:
            return operations[ast_root.val][1](solve(ast_root.left), solve(ast_root.right))


def calculator(string):
    return solve(parser(lexer(string)))


def main():
    DEBUG = False
    prompt = ['Expression > ', 'DEBUG > ']
    try:
        while 1:
            string = input(prompt[DEBUG])
            if string.upper().strip() == 'DEBUG':
                DEBUG = not DEBUG
                continue

            if DEBUG:
                print('Atoms      :', list(zip(*lexer(string)))[1])
                print('Tree       :', repr(parser(lexer(string))))
                print('PyResult   :', eval(string.replace('^', '**')))
                print('MyResult   :', solve(parser(lexer(string)), DEBUG))
            else:
                print('Result:', calculator(string))
    except (EOFError, KeyboardInterrupt):
        exit()


if __name__ == '__main__':
    main()
