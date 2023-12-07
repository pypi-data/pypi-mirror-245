from numpy import mod, pi, sign, sum

from waveforms.waveform import (cos, coshPulse, cosPulse, gaussian,
                                general_cosine, mixing, pi, sin, square, zero)
from waveforms.waveform_parser import wave_eval

from .qlisp2 import (Library, add_phase, add_time, capture, play, set_bias, set_time,
                     set_phase)

EPS = 1e-9

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


@lib.gate('P')
def P(ctx, qubits, phi):
    qubit, = qubits
    yield from add_phase(qubit, phi)


@lib.gate('Delay')
def delay(ctx, qubits, time):
    qubit, = qubits
    yield from add_time(qubit, time)


@lib.gate('Barrier')
def barrier(ctx, qubits):
    time = max(ctx.time[qubit] for qubit in qubits)
    for qubit in qubits:
        yield ('!set_time', time), qubit


@lib.gate()
def U(q, theta, phi, lambda_):
    yield (('R', -lambda_), q)
    yield (('R', -pi - theta - lambda_), q)
    yield (('P', theta + phi + lambda_), q)


@lib.gate()
def u3(qubit, theta, phi, lambda_):
    yield (('U', theta, phi, lambda_), qubit)


@lib.gate()
def u2(qubit, phi, lambda_):
    yield (('U', pi / 2, phi, lambda_), qubit)


@lib.gate()
def u1(qubit, lambda_):
    yield (('P', lambda_), qubit)


@lib.gate()
def H(qubit):
    yield (('u2', 0, pi), qubit)


@lib.gate()
def I(q):
    yield (('u3', 0, 0, 0), q)


@lib.gate()
def X(q):
    yield (('u3', pi, 0, pi), q)


@lib.gate()
def Y(q):
    yield (('u3', pi, pi / 2, pi / 2), q)


@lib.gate()
def Z(q):
    yield (('u1', pi), q)


@lib.gate()
def S(q):
    yield (('u1', pi / 2), q)


@lib.gate(name='-S')
def Sdg(q):
    yield (('u1', -pi / 2), q)


@lib.gate()
def T(q):
    yield (('u1', pi / 4), q)


@lib.gate(name='-T')
def Tdg(q):
    yield (('u1', -pi / 4), q)


@lib.gate(name='X/2')
def sx(q):
    yield ('-S', q)
    yield ('H', q)
    yield ('-S', q)


@lib.gate(name='-X/2')
def sxdg(q):
    yield ('S', q)
    yield ('H', q)
    yield ('S', q)


@lib.gate(name='Y/2')
def sy(q):
    yield ('Z', q)
    yield ('H', q)


@lib.gate(name='-Y/2')
def sydg(q):
    yield ('H', q)
    yield ('Z', q)


@lib.gate()
def Rx(q, theta):
    yield (('u3', theta, -pi / 2, pi / 2), q)


@lib.gate()
def Ry(q, theta):
    yield (('u3', theta, 0, 0), q)


@lib.gate(name='W/2')
def W2(q):
    yield (('u3', pi / 2, -pi / 4, pi / 4), q)


@lib.gate(name='-W/2')
def W2(q):
    yield (('u3', -pi / 2, -pi / 4, pi / 4), q)


@lib.gate(name='V/2')
def W2(q):
    yield (('u3', pi / 2, -3 * pi / 4, 3 * pi / 4), q)


@lib.gate(name='-V/2')
def W2(q):
    yield (('u3', -pi / 2, -3 * pi / 4, 3 * pi / 4), q)


@lib.gate()
def Rz(q, phi):
    yield (('u1', phi), q)


@lib.gate(2)
def Cnot(qubits):
    c, t = qubits
    yield ('H', t)
    yield ('CZ', (c, t))
    yield ('H', t)


@lib.gate(2)
def crz(qubits, lambda_):
    c, t = qubits

    yield (('u1', lambda_ / 2), t)
    yield ('Cnot', (c, t))
    yield (('u1', -lambda_ / 2), t)
    yield ('Cnot', (c, t))


@lib.opaque('rfPulse')
def rfPulse(ctx, qubits, waveform):
    qubit, = qubits

    if isinstance(waveform, str):
        waveform = wave_eval(waveform)

    yield ('!play', waveform >> ctx.time[qubit]), ('RF', qubit)


@lib.opaque('fluxPulse')
def fluxPulse(ctx, qubits, waveform):
    qubit, = qubits

    if isinstance(waveform, str):
        waveform = wave_eval(waveform)

    yield ('!play', waveform >> ctx.time[qubit]), ('Z', qubit)


@lib.opaque('Pulse')
def Pulse(ctx, qubits, channel, waveform):

    if isinstance(waveform, str):
        waveform = wave_eval(waveform)

    t = max(ctx.time[qubit] for qubit in qubits)

    yield ('!play', waveform >> t), (channel, *qubits)


@lib.opaque('setBias')
def setBias(ctx, qubits, channel, bias, edge=0, buffer=0):
    if channel.startswith('coupler.') and len(qubits) == 2:
        qubits = sorted(qubits)
    yield ('!set_bias', (bias, edge, buffer)), (channel, *qubits)
    time = max(ctx.time[qubit] for qubit in qubits)
    for qubit in qubits:
        yield ('!set_time', time + buffer), qubit


@lib.opaque('CZ')
def CZ(ctx, qubits):
    t = max(ctx.time[q] for q in qubits)

    widthq = ctx.params.get('width', 10e-9)
    ampc = ctx.params.get('ampc', 0)
    amp1 = ctx.params.get('amp1', 0)
    amp2 = ctx.params.get('amp2', 0)
    eps = ctx.params.get('eps', 1.0)
    plateauq = ctx.params.get('plateau', 0.0)
    widthc = ctx.params.get('widthc', widthq)
    plateauc = ctx.params.get('plateauc', plateauq)
    buffer = ctx.params.get('buffer', 0.0)
    netzero = ctx.params.get('netzero', False)
    flip = ctx.params.get('flip', False)

    if netzero:
        duration = 2 * max(widthq, widthc) + 2 * max(plateauq,
                                                     plateauc) + buffer
    else:
        duration = max(widthq, widthc) + max(plateauq, plateauc) + buffer

    for amp, width, plateau, target in zip([ampc, amp1, amp2],
                                           [widthc, widthq, widthq],
                                           [plateauc, plateauq, plateauq],
                                           [('coupler.Z', *qubits),
                                            ('Z', qubits[0]),
                                            ('Z', qubits[1])]):
        sign = ctx.scopes[0].setdefault(('CZ_sign', target), 1)
        if amp != 0 and duration > 0:
            pulse = sign * amp * coshPulse(width, plateau=plateau,
                                           eps=eps) >> (width + plateau) / 2
            if netzero:
                pulse += -sign * amp * coshPulse(
                    width, plateau=plateau,
                    eps=eps) >> (width + plateau) * 3 / 2
            yield ('!play', pulse >> t + buffer / 2), target
        if flip:
            ctx.scopes[0][('CZ_sign', target)] = -1 * sign

    for qubit in qubits:
        yield ('!set_time', t + duration), qubit

    yield ('!add_phase', ctx.params.get('phi1', 0)), qubits[0]
    yield ('!add_phase', ctx.params.get('phi2', 0)), qubits[1]

