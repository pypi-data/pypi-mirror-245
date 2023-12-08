from qiskit import *
from qiskit import QuantumCircuit, BasicAer, execute

def qrand(x):
    qr=QuantumRegister(1)
    cr=ClassicalRegister(1)
    circuit=QuantumCircuit(qr,cr)
    circuit.h(qr[0])
    circuit.measure(qr,cr)
    simulator = BasicAer.get_backend('qasm_simulator')
    job = execute(circuit, backend=simulator, shots=x, memory=True)
    data = job.result().get_memory()
    bitString = ' '.join(str(e) for e in data)
    bitString = bitString.replace(" ", "")
    num = int(bitString, 2)
    # convert int to hexadecimal
    hex_qrn = format(num, 'x')

    return hex_qrn