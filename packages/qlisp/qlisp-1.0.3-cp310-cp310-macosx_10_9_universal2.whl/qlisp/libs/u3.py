import re

from numpy import mod, pi, sign, sum
from waveforms.waveform import coshPulse, gaussian, general_cosine, mixing, pi

from qlisp import Library, add_VZ_rule

EPS = 1e-9

lib = Library()


def _VZ_R(st, phaseList):
    (_, phi, *with_params), qubit = st
    return [(('R', mod(phi - phaseList[0],
                       2 * pi), *with_params), qubit)], phaseList


add_VZ_rule('R', _VZ_R)


def get_frequency_phase(ctx, qubit, phi, level1, level2):
    freq = ctx.params.get('frequency', ctx.params.get('freq', 0.5))
    phi = mod(
        phi + ctx.phases_ext[qubit][level1] - ctx.phases_ext[qubit][level2],
        2 * pi)
    phi = phi if abs(level2 - level1) % 2 else phi - pi
    if phi > pi:
        phi -= 2 * pi
    phi = phi / (level2 - level1)

    return freq, phi


def DRAG(t, shape, width, plateau, eps, amp, alpha, beta, delta, freq, phase):
    from waveforms.waveform import drag

    if shape in ['hanning', 'cosPulse', 'CosPulse']:
        if beta == 0:
            block_freq = None
        else:
            block_freq = -1 / (2 * pi) / (beta / alpha)
        return (amp * alpha) * drag(freq, width, plateau, delta, block_freq,
                                    phase, t - width / 2 - plateau / 2)
    elif shape in ['coshPulse', 'CoshPulse']:
        pulse = coshPulse(width, plateau=plateau, eps=eps)
    else:
        pulse = gaussian(width, plateau=plateau)
    I, Q = mixing(amp * alpha * pulse,
                  phase=phase,
                  freq=delta,
                  DRAGScaling=beta / alpha)
    wav, _ = mixing(I >> t, Q >> t, freq=freq)
    return wav


def R(ctx, qubits, phi=0, level1=0, level2=1):
    qubit, = qubits

    freq, phase = get_frequency_phase(ctx, qubit, phi, level1, level2)

    amp = ctx.params.get('amp', 0.5)
    shape = ctx.params.get('shape', 'cosPulse')
    width = ctx.params.get('width', 5e-9)
    plateau = ctx.params.get('plateau', 0.0)
    buffer = ctx.params.get('buffer', 0)

    duration = width + plateau + buffer
    if amp != 0:
        alpha = ctx.params.get('alpha', 1)
        beta = ctx.params.get('beta', 0)
        delta = ctx.params.get('delta', 0)
        eps = ctx.params.get('eps', 1)
        channel = ctx.params.get('channel', 'RF')
        t = duration / 2 + ctx.time[qubit]

        if shape == 'S1':
            arg = ctx.params.get('arg', [-2.253, 0.977, 1.029])
            pulse = general_cosine(width, *arg) * sign(-sum(arg[::2]))
            I, Q = mixing(amp * alpha * pulse,
                          phase=phase,
                          freq=delta,
                          DRAGScaling=beta / alpha)
            wav, _ = mixing(I >> t, Q >> t, freq=freq)
        wav = DRAG(t, shape, width, plateau, eps, amp, alpha, beta, delta,
                   freq, phase)
        yield ('!play', wav), (channel, qubit)
    yield ('!add_time', duration), qubit


@lib.opaque('R')
def _R(ctx, qubits, phi=0):
    yield from R(ctx, qubits, phi, 0, 1)


@lib.opaque('R12')
def _R12(ctx, qubits, phi=0):
    yield from R(ctx, qubits, phi, 1, 2)


@lib.opaque('R23')
def _R23(ctx, qubits, phi=0):
    yield from R(ctx, qubits, phi, 2, 3)


@lib.opaque('P')
def P(ctx, qubits, phi):
    import numpy as np

    from qlisp.assembly import call_opaque

    phi += ctx.phases[qubits[0]]
    yield ('!set_phase', 0), qubits[0]
    x = 2 * np.pi * np.random.random()
    y = np.pi * np.random.randint(0, 2) + x

    call_opaque((('R', x), qubits), ctx, lib)
    call_opaque((('R', x), qubits), ctx, lib)
    call_opaque((('R', phi / 2 + y), qubits), ctx, lib)
    call_opaque((('R', phi / 2 + y), qubits), ctx, lib)


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
