from z3 import *  # noqa
from z3 import (
    Abs,
    And,
    BitVec,
    BitVecRef,
    Extract,
    If,
    LShR,
    ModelRef,
    Not,
    sat,
    Solver,
    unknown,
    unsat,
)


class Z3SolveException(Exception):
    pass


class Z3Unsat(Z3SolveException):
    pass


class Z3Unknown(Z3SolveException):
    pass


class Z3CounterExample(Z3SolveException):
    model: ModelRef

    def __init__(self, model: ModelRef):
        super().__init__(model)
        self.model = model


def easy_solve(constraints):
    solver = Solver()
    solver.add(*constraints)
    res = solver.check()
    if res == unsat:
        raise Z3Unsat
    elif res == unknown:
        raise Z3Unknown

    return solver.model()


def find_all_solutions(constraints):
    """
    >>> def normalize_result(r):
    ...     return sorted(sorted((f.name(), m[f].as_long()) for f in m) for m in r)
    >>> a, b, c = Ints("a b c")
    >>> normalize_result(find_all_solutions([0 <= a, a < 3]))
    [[('a', 0)], [('a', 1)], [('a', 2)]]
    >>> normalize_result(find_all_solutions([0 <= a, a < 2, b == 2 * a]))
    [[('a', 0), ('b', 0)], [('a', 1), ('b', 2)]]
    """
    solver = Solver()
    solver.add(*constraints)
    while True:
        res = solver.check()
        if res == unknown:
            raise Z3Unknown
        elif res == unsat:
            return

        model = solver.model()
        yield model

        solver.add(Not(And([f() == model[f] for f in model if f.arity() == 0])))


def easy_prove(claim):
    solver = Solver()
    solver.add(Not(claim))
    res = solver.check()
    if res == unknown:
        raise Z3Unknown
    elif res == sat:
        raise Z3CounterExample(solver.model())
    else:
        return True


BitVecRef.__rshift__ = LShR
BitVecRef.__rrshift__ = lambda a, b: LShR(b, a)


class ByteVec(BitVecRef):
    def __init__(self, name, byte_count, ctx=None):
        self.byte_count = byte_count
        self.bv = BitVec(name, byte_count * 8, ctx)

    def __getattr__(self, attr):
        return getattr(self.bv, attr)

    def __len__(self):
        return self.byte_count

    def __getitem__(self, i):
        if not isinstance(i, int):
            raise TypeError

        if i < 0:
            i += len(self)

        if not (0 <= i < len(self)):
            raise IndexError

        return Extract(8 * i + 7, 8 * i, self.bv)

    def value(self, model):
        v = model[self.bv].as_long()
        return v.to_bytes(self.byte_count, "little")


def BoolToInt(x):
    return If(x, 1, 0)


def Sgn(x):
    return If(x == 0, 0, If(x > 0, 1, -1))


def TruncDiv(a, b):
    """
    Truncated division, a / b rounded towards zero.

    >>> a, b, c = Ints("a b c")
    >>> easy_prove(Implies(TruncDiv(a, b) == c, Abs(b) * Abs(c) <= Abs(a)))
    True
    """
    v = Abs(a) / Abs(b)
    return Sgn(a) * Sgn(b) * v
