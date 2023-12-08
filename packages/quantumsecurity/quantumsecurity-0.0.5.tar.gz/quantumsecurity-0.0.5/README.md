# QuantumSecurity

[![PyPI version](https://badge.fury.io/py/quantumsecurity.svg)](https://badge.fury.io/py/quantumsecurity)

A Python package for supporting security applications with the power of quantum computing and cryptography.

## Description

QuantumSecurity is a Python package designed to assist developers in implementing security applications using quantum computing and cryptography. The package currently provides a function named `qrand` that generates quantum random numbers. The generated quantum random numbers are in hexadecimal format.

## Installation

You can install QuantumSecurity using pip:

```bash
pip install quantumsecurity

## Usage
from quantumsecurity import qrand

# Generate a quantum random number with 16 bits
random_number = qrand(16)
print("Quantum Random Number:", random_number)

## Dependencies
The current version of QuantumSecurity relies on the Qiskit package and its 'qasm_simulator' for quantum random number generation. In future iterations, support for other simulators from Amazon Braket and Quantum Hardware facilities will be added to the 'qrand' function.

## Future Features
In future releases, QuantumSecurity aims to provide additional dynamic functions related to quantum cryptography and post-quantum cryptography. These functions will empower developers to streamline their security implementations without writing extensive code.