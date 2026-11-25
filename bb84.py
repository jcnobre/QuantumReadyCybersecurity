import random
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer, AerSimulator
from qiskit import transpile

n_qubits = 10

# Step 1 - Alice choses randomly the bits and the bases
alice_bits = [random.randint(0,1) for _ in range(n_qubits)]
alice_bases = [random.choice(['Z', 'X']) for _ in range(n_qubits)]

#Step 2 - Bob Choses randomly measurement basis
bob_bases = [random.choice(['Z', 'X']) for _ in range(n_qubits)]

bob_results = []

# We will use a simulator to run the circuit
backend = Aer.get_backend('qasm_simulator')

#For each qbit create a quantum curcuit to simulate state preparation and measurements
for i in range(n_qubits):

  qc = QuantumCircuit(1,1) #one quantum bit and one classical bit
  # ----------- Alice state circuit preparation
  if alice_bases[i] == 'Z':
    ## In the Z basis, bit 0 is |0> and bit 1 is |1>
    ## If the bit is 1 flip it
    if alice_bits[i] == 1:
      qc.x(0)
  else:
    ## For the X basis, prepare |+> for bit 0 and |-> for bit 1.
    if alice_bits[i] == 0:
      qc.h(0)
    else:
      qc.x(0)
      qc.h(0)

## State Preparation Details:
## - When using the Z basis (computational basis), a bit 0 is encoded as |0⟩ and a bit 1 as |1⟩ (by applying an X gate).
## - When using the X basis (diagonal basis), a bit 0 is encoded as |+⟩ and a bit 1 as |−⟩.
##
## The Hadamard gate (H) is used to transform computational basis states into diagonal basis states:
##   H|0⟩ = |+⟩  and  H|1⟩ = |−⟩.
##
## This transformation is crucial in quantum key distribution protocols (e.g., BB84). If a qubit prepared in one basis
## is measured in a different basis, the measurement outcome becomes random (with a 50-50 probability), which is a key
## property that ensures the security of the protocol.

  ## Bob's measurements

  # if Bob's base is X apply Hadamard to prepare for measurements
  # Notice that there is a 50 - 50 chance of the qbit collapsing as 0 or 1
  if bob_bases[i] == 'X':
    qc.h(0)

  qc.measure(0,0)

  new_cirq = transpile(qc, backend)
  job = backend.run(new_cirq)

  counts = job.result().get_counts()

  measured_bit = int(list(counts.keys())[0])
  bob_results.append(measured_bit)

# Alice and Bob reveal their bases over a public channel and only keep the bits where their bases match
sifted_key = []
for i in range(n_qubits):
  if alice_bases[i] == bob_bases[i]:
    sifted_key.append(alice_bits[i])
    print(f"Qubit {i}: Basis match ({alice_bases[i]}). Alice's bit: {alice_bits[i]}, Bob's measurement: {bob_results[i]}")
  else:
    print(f"Qubit {i}: Basis mismatch ({alice_bases[i]}). Alice's bit: {alice_bits[i]}, Bob's measurement: {bob_results[i]}")
  
print("\nFinal sifted key:", sifted_key)