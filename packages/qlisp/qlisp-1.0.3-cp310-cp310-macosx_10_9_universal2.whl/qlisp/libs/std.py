from waveforms.waveform import zero
from waveforms.waveform_parser import wave_eval

from qlisp import Library, add_VZ_rule

EPS = 1e-9

lib = Library()


def _VZ_commutable(st, phaseList):
    return [st], phaseList


add_VZ_rule('Delay', _VZ_commutable)
add_VZ_rule('Barrier', _VZ_commutable)
add_VZ_rule('Pulse', _VZ_commutable)
add_VZ_rule('rfPulse', _VZ_commutable)
add_VZ_rule('fluxPulse', _VZ_commutable)
add_VZ_rule('setBias', _VZ_commutable)


@lib.opaque('Delay')
def delay(ctx, qubits, time):
    qubit, = qubits
    yield ('!play', zero()), ('RF', qubit)
    yield ('!play', zero()), ('Z', qubit)
    yield ('!play', zero()), ('readoutLine.RF', qubit)
    yield ('!add_time', time), qubit


@lib.opaque('Barrier')
def barrier(ctx, qubits):
    time = max(ctx.time[qubit] for qubit in qubits)
    for qubit in qubits:
        yield ('!set_time', time), qubit


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
