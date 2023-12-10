from __future__ import annotations

import re
from decimal import Decimal
from operator import add, mod, mul, pow, sub, truediv
from typing import Callable


class Sign:
    pass


class Operator(Sign):
    def __init__(self, op: Convertor, count=2, priority=1):
        self.op = op
        self.count = count
        self.priority = priority

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.op.__name__}, priority={self.priority})'

    def calc(self, *args: Decimal):
        if len(args) != self.count:
            raise ValueError
        return self.op(*args)

    __repr__ = __str__


class Bracket(Sign):
    def __init__(self, pair: str | None = None, is_head=False):
        self.pair = pair
        self.is_head = is_head

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(pair={repr(self.pair)})'

    __repr__ = __str__


Convertor = Callable[..., Decimal]

signs: dict[str | re.Pattern, Convertor | Operator | Bracket] = {
    re.compile(r'-?\d+(\.\d+)?'): Decimal,
    '+': Operator(add),
    '-': Operator(sub),
    '*': Operator(mul, priority=2),
    'x': Operator(mul, priority=2),
    '/': Operator(truediv, priority=2),
    '÷': Operator(truediv, priority=2),
    '%': Operator(mod, priority=2),
    'mod': Operator(mod, priority=2),
    '^': Operator(pow, priority=3),
    '(': Bracket('()', is_head=True),
    ')': Bracket('()'),
    '[': Bracket('[]', is_head=True),
    ']': Bracket('[]'),
}


def parse_sign(expression: str):
    """解析表达式并返回解析后的结果"""
    for pattern, op in signs.items():
        if isinstance(pattern, str):
            if not expression.startswith(pattern):
                continue
            return op, len(pattern)
        else:
            span = pattern.match(expression)
            if span is None:
                continue
            return op, span.end()
    raise ValueError("不支持的符号")


def calc(expression: str) -> Decimal:
    return calc_preprocessed(preprocess(expression))


def preprocess(expression: str) -> list[Decimal | Operator]:
    stack: list[Operator | Bracket] = []
    preprocessed: list[Decimal | Operator] = []

    expression.strip()
    while expression:
        sign, length = parse_sign(expression)
        if not isinstance(sign, Sign):
            preprocessed.append(sign(expression[:length]))
        elif isinstance(sign, Operator):
            while stack and isinstance(stack[-1], Operator) and stack[-1].priority >= sign.priority:
                preprocessed.append(stack[-1])
                del stack[-1]
            stack.append(sign)
        else:
            if sign.is_head:
                stack.append(sign)
            else:
                while isinstance(stack[-1], Operator):
                    preprocessed.append(stack[-1])
                    del stack[-1]
                if isinstance(stack[-1], Bracket) and stack[-1].pair != sign.pair:
                    raise ValueError("不匹配的括号")
                del stack[-1]
        expression = expression[length:].strip()

    preprocessed.extend(reversed([i for i in stack if isinstance(i, Operator)]))
    return preprocessed


def calc_preprocessed(preprocessed: list[Decimal | Operator]):
    stack: list[Decimal] = []
    for sign in preprocessed:
        if isinstance(sign, Operator):
            if len(stack) < sign.count:
                raise ValueError("表达式错误")
            result = sign.calc(*stack[-sign.count:])
            stack = stack[:-sign.count]
            stack.append(result)
        else:
            stack.append(sign)

    if len(stack) != 1:
        raise ValueError("表达式错误")
    return stack[0]


def main():
    result = calc("1 + (0.1 + 0.2) * 3 / 3")
    print(result)


if __name__ == "__main__":
    main()
