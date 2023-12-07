import inspect
import math
from collections import defaultdict
from enum import Enum, auto
from functools import partial
from typing import Any, Callable, NamedTuple, Self

Decorator = Callable[[Callable], Callable]


class OPCODE(Enum):
    # Register commands
    PUSH_SP = auto()
    PUSH_BP = auto()
    PUSH_SL = auto()
    PUSH_PC = auto()
    SET_SP = auto()
    SET_BP = auto()
    SET_SL = auto()
    SET_PC = auto()

    # Control operators
    NOP = auto()
    PUSH = auto()
    DUP = auto()
    DROP = auto()
    SWAP = auto()
    OVER = auto()
    SLOAD = auto()
    SSTORE = auto()
    LOAD = auto()
    STORE = auto()
    CALL = auto()
    RET = auto()
    CALL_RET = auto()
    JMP = auto()
    JNZ = auto()
    JZ = auto()
    EXIT = auto()

    # Quantum operators
    PLAY = auto()
    CAPTURE = auto()
    CAPTURE_IQ = auto()
    CAPTURE_TRACE = auto()
    SET_TIME = auto()
    SET_PHASE = auto()
    SET_PHASE_EXT = auto()
    SET_BIAS = auto()
    ADD_TIME = auto()
    ADD_PHASE = auto()
    ADD_PHASE_EXT = auto()
    ADD_BIAS = auto()

    # Hardware control operators
    SET = auto()

    # Arithmetic operators
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    NEG = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    BOR = auto()
    BAND = auto()
    BNOT = auto()
    XOR = auto()
    SHL = auto()
    SHR = auto()

    # Math operators
    ABS = auto()
    SQRT = auto()
    EXP = auto()
    SIN = auto()
    COS = auto()
    TAN = auto()
    ASIN = auto()
    ACOS = auto()
    ATAN = auto()
    ATAN2 = auto()
    LOG = auto()
    POW = auto()
    MIN = auto()
    MAX = auto()

    def __repr__(self):
        return self.name


class Instruction(NamedTuple):
    op: OPCODE
    args: tuple = ()
    label: str | None = None
    trace: tuple = ()


class Channel(NamedTuple):
    qubits: tuple[str, ...]
    type: str


def capture(channel,
            cbit,
            duration,
            function,
            *args,
            label=None,
            trace=()) -> Instruction:
    """
    Capture a waveform from a channel.

    Args:
        channel: The channel to capture.
        cbit: The label of the result.
    """
    yield Instruction(OPCODE.CAPTURE,
                      (channel, cbit, duration, function, *args),
                      label=label,
                      trace=trace)


def play(channel,
         shape,
         frequency,
         phase,
         *args,
         label=None,
         trace=()) -> Instruction:
    yield Instruction(OPCODE.PLAY, (channel, shape, frequency, phase, *args),
                      label=label,
                      trace=trace)


def set_time(channel, time, label=None, trace=()) -> Instruction:
    yield Instruction(OPCODE.PUSH, (time, ), label=label, trace=trace)
    yield Instruction(OPCODE.SET_TIME, (channel, ), label=label, trace=trace)


def set_phase(channel, frequency, phase, label=None, trace=()) -> Instruction:
    yield Instruction(OPCODE.PUSH, (phase, ), label=label, trace=trace)
    yield Instruction(OPCODE.PUSH, (frequency, ), label=label, trace=trace)
    yield Instruction(OPCODE.SET_PHASE, (channel, ), label=label, trace=trace)


def set_phase_ext(channel,
                  frequency,
                  phase,
                  label=None,
                  trace=()) -> Instruction:
    yield Instruction(OPCODE.PUSH, (phase, ), label=label, trace=trace)
    yield Instruction(OPCODE.PUSH, (frequency, ), label=label, trace=trace)
    yield Instruction(OPCODE.SET_PHASE_EXT, (channel, ),
                      label=label,
                      trace=trace)


def set_bias(channel, bias, label=None, trace=()) -> Instruction:
    yield Instruction(OPCODE.SET_BIAS, (channel, bias),
                      label=label,
                      trace=trace)


def set_instrument(channel, key, value, label=None, trace=()) -> Instruction:
    yield Instruction(OPCODE.SET, (channel, key, value),
                      label=label,
                      trace=trace)


def add_time(channel, time, label=None, trace=()) -> Instruction:
    yield Instruction(OPCODE.ADD_TIME, (channel, time),
                      label=label,
                      trace=trace)


def add_phase(channel, frequency, phase, label=None, trace=()) -> Instruction:
    yield Instruction(OPCODE.ADD_PHASE, (channel, frequency, phase),
                      label=label,
                      trace=trace)


def add_phase_ext(channel,
                  frequency,
                  phase,
                  label=None,
                  trace=()) -> Instruction:
    yield Instruction(OPCODE.ADD_PHASE_EXT, (channel, frequency, phase),
                      label=label,
                      trace=trace)


def add_bias(channel, bias, label=None, trace=()) -> Instruction:
    yield Instruction(OPCODE.PUSH, (bias, ), label=label, trace=trace)
    yield Instruction(OPCODE.ADD_BIAS, (channel, ), label=label, trace=trace)


def nop(label=None, trace=()) -> Instruction:
    yield Instruction(OPCODE.NOP, label=label, trace=trace)


class Config():

    def get(self, key):
        pass

    def get_gate(self, name, qubits, type=None) -> dict[str, Any]:
        pass


class Library():

    def __init__(self):
        self.parent = None
        self.namespace = {}

    def get(self, name: str, type: str | None = None):
        if name not in self.namespace and self.parent is None:
            raise KeyError(f'can not find {name!r} in library.')
        if type is None:
            if name in self.namespace:
                return self.namespace[name]
            else:
                return self.parent.get(name)

        if name in self.namespace:
            if type == 'default':
                type_ = self.namespace[name].get('__default_type__', 'default')
            if type_ not in self.namespace[name]:
                raise KeyError(f'can not find {name!r} with type {type_!r}.')
            return self.namespace[name][type_]
        return self.parent.get(name, type)

    def gate(self,
             name: str | Callable | None = None,
             type='default') -> Decorator | Callable:
        if callable(name):
            return self.gate()(name)

        def decorator(func, name=name, type=type):
            if name is None:
                if isinstance(func, partial):
                    name = func.func.__name__
                else:
                    name = func.__name__
                if name not in self.namespace:
                    self.namespace[name] = {'__default_type__': 'default'}
                if type == 'default':
                    type = self.namespace[name].get('__default_type__',
                                                    'default')
            self.namespace[name][type] = func
            return func

        return decorator


lib = Library()


@lib.gate('R')
def R(qubits, phi, params, ctx):
    yield from play(qubits[0], 'gaussian', 0, 0)
    yield from set_phase(qubits[0], 0, phi)


@lib.gate('Measure')
def Measure(qubits, cbit, params, ctx):
    duration = params.get('duration', 1e-6)
    function = params.get('function', 'threshold')
    threshold = params.get('threshold', 0)
    phi = params.get('phi', 0)

    yield from play(qubits[0], 'gaussian', 0, 0)
    yield from set_phase(qubits[0], 0, 0)
    yield from capture(qubits[0], cbit, duration, function, threshold, phi)


class Contex():

    def __init__(self, cfg: Config, lib: Library):
        self.scopes = []
        self.cfg = cfg
        self.lib = lib

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        try:
            self.cfg.get(name)
        except:
            raise KeyError(f'can not find {name!r} in scopes.')


def head(statement) -> str | type:
    """
    Return the head of a statement.
    """
    if not isinstance(statement, tuple):
        return type(statement)
    name = statement[0]
    if isinstance(name, str):
        return name
    elif isinstance(name, tuple):
        return head(name)
    else:
        return tuple


def call_gate(gate: str | tuple, qubits: tuple, lib: Library, ctx: Contex):
    func, args, params, others = parse_gate(gate, qubits, ctx)
    ctx.scopes.append(params)
    for instruction in func(qubits, *args, ctx.scopes[-1], ctx):
        if isinstance(instruction, Instruction):
            yield instruction
        else:
            yield from call_gate(instruction, qubits, lib, ctx)
    ctx.scopes.pop()


def parse_gate(gate, qubits: tuple, ctx: Contex):
    if isinstance(gate, str):
        args = ()
        name = gate
    else:
        name, *args = gate
        if isinstance(args[-1], tuple) and head(args[-1]) == 'with':
            args, (params, others) = tuple(args[:-1]), parse_with_statement(
                args[-1], ctx.cfg)
        else:
            args = tuple(args)
            params = {}
            others = {}
    gate_params = ctx.cfg.get_gate(name, qubits, others.get('type', 'default'))
    kwds = gate_params.copy()
    kwds.update({k: v for k, v in params.items() if not callable(v)})
    for k, v in gate_params.items():
        if k not in params:
            params[k] = v
    params = {k: _try_to_call(v, kwds) for k, v in params.items()}
    func = ctx.lib.get(head(gate), others.get('type', 'default'))
    return func, args, params, others


def _call_func_with_kwds(func, kwds):
    sig = inspect.signature(func)
    for p in sig.parameters.values():
        if p.kind == p.VAR_KEYWORD:
            return func(**kwds)
    kw = {k: v for k, v in kwds.items() if k in sig.parameters}
    return func(**kw)


def _try_to_call(x, kwds):
    if callable(x):
        return _call_func_with_kwds(x, kwds)
    return x


def parse_with_statement(statement, cfg: Config):
    params = {}
    others = {}
    for k, v in statement[1:]:
        if k.startswith('param:'):
            if isinstance(v, str) and v.startswith('cfg:'):
                v = cfg.get(v[4:])
            params[k[6:]] = v
        else:
            others[k] = v
    return params, others


class VirtualMachineExit(Exception):
    pass


class VirtualMachine():

    def __init__(self):
        self.channels = defaultdict(list)
        self.waveforms = {}
        self.captures = {}
        self.time = {}
        self.phase = {}

        self.stack = []
        self.mem = []
        self.sp = 0  # stack pointer
        self.bp = 0  # base pointer
        self.sl = 0  # static link
        self.pc = 0  # program counter
        self.clk = 0  # clock

        self.dispatch = {
            OPCODE.NOP: self.nop,
            OPCODE.PUSH_SP: self.push_sp,
            OPCODE.PUSH_BP: self.push_bp,
            OPCODE.PUSH_SL: self.push_sl,
            OPCODE.PUSH_PC: self.push_pc,
            OPCODE.SET_SP: self.set_sp,
            OPCODE.SET_BP: self.set_bp,
            OPCODE.SET_SL: self.set_sl,
            OPCODE.SET_PC: self.set_pc,
            OPCODE.PUSH: self.push,
            OPCODE.DUP: self.dup,
            OPCODE.DROP: self.drop,
            OPCODE.SWAP: self.swap,
            OPCODE.OVER: self.over,
            OPCODE.SLOAD: self.sload,
            OPCODE.SSTORE: self.sstore,
            OPCODE.LOAD: self.load,
            OPCODE.STORE: self.store,
            OPCODE.CALL: self.call,
            OPCODE.RET: self.ret,
            OPCODE.CALL_RET: self.call_ret,
            OPCODE.JMP: self.jmp,
            OPCODE.JNZ: self.jnz,
            OPCODE.JZ: self.jz,
            OPCODE.EXIT: self.exit,
            OPCODE.PLAY: self.play,
            OPCODE.CAPTURE: self.capture,
            OPCODE.SET_TIME: self.set_time,
            OPCODE.SET_PHASE: self.set_phase,
            OPCODE.SET_PHASE_EXT: self.set_phase_ext,
            OPCODE.SET_BIAS: self.set_bias,
            OPCODE.ADD_TIME: self.add_time,
            OPCODE.ADD_PHASE: self.add_phase,
            OPCODE.ADD_PHASE_EXT: self.add_phase_ext,
            OPCODE.ADD_BIAS: self.add_bias,
            OPCODE.SET: self.set,
            OPCODE.ADD: self.add,
            OPCODE.SUB: self.sub,
            OPCODE.MUL: self.mul,
            OPCODE.DIV: self.div,
            OPCODE.MOD: self.mod,
            OPCODE.NEG: self.neg,
            OPCODE.EQ: self.eq,
            OPCODE.NE: self.ne,
            OPCODE.LT: self.lt,
            OPCODE.LE: self.le,
            OPCODE.GT: self.gt,
            OPCODE.GE: self.ge,
            OPCODE.AND: self.and_,
            OPCODE.OR: self.or_,
            OPCODE.NOT: self.not_,
            OPCODE.BOR: self.bor,
            OPCODE.BAND: self.band,
            OPCODE.BNOT: self.bnot,
            OPCODE.XOR: self.xor,
            OPCODE.SHL: self.shl,
            OPCODE.SHR: self.shr,
            OPCODE.ABS: self.abs,
            OPCODE.SQRT: self.sqrt,
            OPCODE.EXP: self.exp,
            OPCODE.SIN: self.sin,
            OPCODE.COS: self.cos,
            OPCODE.TAN: self.tan,
            OPCODE.ASIN: self.asin,
            OPCODE.ACOS: self.acos,
            OPCODE.ATAN: self.atan,
            OPCODE.ATAN2: self.atan2,
            OPCODE.LOG: self.log,
            OPCODE.POW: self.pow,
            OPCODE.MIN: self.min,
            OPCODE.MAX: self.max,
        }

    def next(self):
        self.pc += 1
        try:
            return self.mem[self.pc - 1]
        except IndexError:
            return Instruction(OPCODE.EXIT)

    def pop(self):
        self.sp -= 1
        return self.stack[self.sp]

    def push(self, value):
        if len(self.stack) > self.sp:
            self.stack[self.sp] = value
        else:
            self.stack.append(value)
        self.sp += 1

    def pick(self, n=0):
        return self.stack[self.sp - n - 1]

    def run(self, step_limit=-1):
        self.sp = 0  # stack pointer
        self.bp = 0  # base pointer
        self.sl = 0  # static link
        self.pc = 0  # program counter
        self.clk = 0  # clock
        while True:
            if self.clk == step_limit:
                break
            self.clk += 1
            instruction = self.next()
            self.dispatch[instruction.op](*instruction.args)

    def nop(self):
        pass

    def push_sp(self):
        self.push(self.sp)

    def push_bp(self):
        self.push(self.bp)

    def push_sl(self):
        self.push(self.sl)

    def push_pc(self):
        self.push(self.pc)

    def set_sp(self):
        self.sp = self.pop()

    def set_bp(self):
        self.bp = self.pop()

    def set_sl(self):
        self.sl = self.pop()

    def set_pc(self):
        self.pc = self.pop()

    def dup(self):
        self.push(self.pick())

    def drop(self):
        self.pop()

    def swap(self):
        a = self.pop()
        b = self.pop()
        self.push(a)
        self.push(b)

    def over(self):
        self.push(self.pick(1))

    def sload(self):
        level = self.pop()
        n = self.pop()
        addr = self.bp
        for _ in range(level):
            addr = self.stack[addr - 3]
        self.push(self.stack[addr + n])

    def sstore(self):
        level = self.pop()
        n = self.pop()
        value = self.pop()

        addr = self.bp
        for _ in range(level):
            addr = self.stack[addr - 3]
        self.stack[addr + n] = value

    def load(self):
        self.push(self.mem[self.bp + self.pop()])

    def store(self):
        self.mem[self.bp + self.pop()] = self.pop()

    def call(self):
        func = self.pop()
        argc = self.pop()
        args = [self.pop() for _ in range(argc)]

        if callable(func):
            self.push(func(*args))
        elif isinstance(func, int):
            self.push(self.bp)
            self.push(self.sl)
            self.push(self.pc)
            self.bp = self.sp
            for arg in reversed(args):
                self.push(arg)
            self.sl = func
            self.pc = func
        else:
            raise RuntimeError(f"not callable {func}")

    def ret(self):
        result = self.pop()
        self.sp = self.bp - 3
        self.bp, self.sl, self.pc = self.stack[self.bp - 3:self.bp]
        self.push(result)

    def call_ret(self):
        func = self.pop()
        argc = self.pop()

        if callable(func):
            args = reversed(self.stack[self.sp - argc:self.sp])
            self.sp = self.bp - 3
            self.bp, self.sl, self.pc = self.stack[self.bp - 3:self.bp]
            self.push(func(*args))
        elif isinstance(func, int):
            if self.sp != self.bp + argc:
                self.stack[self.bp:self.bp + argc] = self.stack[self.sp -
                                                                argc:self.sp]
                self.sp = self.bp + argc
            self.sl = func
            self.pc = func
        else:
            raise RuntimeError(f"not callable {func}")

    def jmp(self):
        self.pc = self.pop() + self.sl

    def jnz(self):
        addr = self.pop()
        cond = self.pop()
        if cond:
            self.pc = addr + self.sl

    def jz(self):
        addr = self.pop()
        cond = self.pop()
        if cond == 0:
            self.pc = addr + self.sl

    def exit(self):
        raise VirtualMachineExit()

    def set_time(self, channel):
        time = self.pop()
        self.channels[channel].append((self.clk, OPCODE.SET_TIME, time))

    def set_phase(self, channel):
        frequency = self.pop()
        phase = self.pop()
        self.channels[channel].append(
            (self.clk, OPCODE.SET_PHASE, frequency, phase))

    def set_phase_ext(self, channel):
        frequency = self.pop()
        phase = self.pop()
        self.channels[channel].append(
            (self.clk, OPCODE.SET_PHASE_EXT, frequency, phase))

    def set_bias(self, channel):
        self.channels[channel].append((self.clk, OPCODE.SET_BIAS))

    def play(self, channel):
        self.channels[channel].append((self.clk, OPCODE.PLAY))

    def capture(self, channel):
        self.channels[channel].append((self.clk, OPCODE.CAPTURE))

    def capture_iq(self, channel):
        self.channels[channel].append((self.clk, OPCODE.CAPTURE_IQ))

    def capture_trace(self, channel):
        self.channels[channel].append((self.clk, OPCODE.CAPTURE_TRACE))

    def add_time(self, channel):
        self.channels[channel].append((self.clk, OPCODE.ADD_TIME))

    def add_phase(self, channel):
        self.channels[channel].append((self.clk, OPCODE.ADD_PHASE))

    def add_phase_ext(self, channel):
        self.channels[channel].append((self.clk, OPCODE.ADD_PHASE_EXT))

    def add_bias(self, channel):
        self.channels[channel].append((self.clk, OPCODE.ADD_BIAS))

    def set(self, channel):
        self.channels[channel].append((self.clk, OPCODE.SET))

    def add(self):
        self.push(self.pop() + self.pop())

    def sub(self):
        self.push(self.pop() - self.pop())

    def mul(self):
        self.push(self.pop() * self.pop())

    def div(self):
        self.push(self.pop() / self.pop())

    def mod(self):
        self.push(self.pop() % self.pop())

    def neg(self):
        self.push(-self.pop())

    def eq(self):
        self.push(self.pop() == self.pop())

    def ne(self):
        self.push(self.pop() != self.pop())

    def lt(self):
        self.push(self.pop() < self.pop())

    def le(self):
        self.push(self.pop() <= self.pop())

    def gt(self):
        self.push(self.pop() > self.pop())

    def ge(self):
        self.push(self.pop() >= self.pop())

    def and_(self):
        self.push(self.pop() and self.pop())

    def or_(self):
        self.push(self.pop() or self.pop())

    def not_(self):
        self.push(not self.pop())

    def bor(self):
        self.push(self.pop() | self.pop())

    def band(self):
        self.push(self.pop() & self.pop())

    def bnot(self):
        self.push(~self.pop())

    def xor(self):
        self.push(self.pop() ^ self.pop())

    def shl(self):
        self.push(self.pop() << self.pop())

    def shr(self):
        self.push(self.pop() >> self.pop())

    def abs(self):
        self.push(abs(self.pop()))

    def sqrt(self):
        self.push(math.sqrt(self.pop()))

    def exp(self):
        self.push(math.exp(self.pop()))

    def sin(self):
        self.push(math.sin(self.pop()))

    def cos(self):
        self.push(math.cos(self.pop()))

    def tan(self):
        self.push(math.tan(self.pop()))

    def asin(self):
        self.push(math.asin(self.pop()))

    def acos(self):
        self.push(math.acos(self.pop()))

    def atan(self):
        self.push(math.atan(self.pop()))

    def atan2(self):
        self.push(math.atan2(self.pop(), self.pop()))

    def log(self):
        self.push(math.log(self.pop()))

    def pow(self):
        self.push(math.pow(self.pop(), self.pop()))

    def min(self):
        self.push(min(self.pop(), self.pop()))

    def max(self):
        self.push(max(self.pop(), self.pop()))
