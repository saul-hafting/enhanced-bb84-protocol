from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import numpy as np

# IMPORTANT: Replace with your actual IBM Quantum API token
# Get your token from: https://quantum-computing.ibm.com/
QiskitRuntimeService.save_account(
    token="YOUR_API_TOKEN_HERE",  # Replace with your actual token
    channel="ibm_quantum",
    overwrite=True
)

def QRNG(n_bits):
    """
    Quantum Random Number Generator using superposition and measurement.
    
    Args:
        n_bits (int): Number of random bits to generate
        
    Returns:
        list: List of random bits (0s and 1s)
    """
    circuit = QuantumCircuit(n_bits, n_bits)
    circuit.h(range(n_bits))  # Create superposition states
    circuit.measure(range(n_bits), range(n_bits))  # Collapse to random states
    
    service = QiskitRuntimeService(channel="ibm_quantum", instance="ibm-q/open/main")
    backend = service.least_busy(operational=True, simulator=False)
    sampler = Sampler(mode=backend)
    transpiled_circuit = transpile(circuit, backend)
    
    job = sampler.run([transpiled_circuit], shots=1)
    result = job.result()
    dist = result[0].data.c.get_counts()
    bitstring = list(dist.keys())[0]
    
    return [int(b) for b in bitstring]


# Encoding function
def encode_message(bits, bases):
    circuits = []
    for bit, basis in zip(bits, bases):
        qc = QuantumCircuit(1, 1)
        # Z-basis: apply X 
        if basis == 0:
            if bit == 1:
                qc.x(0)
        # X-basis: prepare state by applying H & X 
        else:
            if bit == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        circuits.append(qc)
    return circuits

# Measurement function
def measure_message(circuits, bases):
    measured_circuits = []
    for qc, basis in zip(circuits, bases):
        measured_qc = qc.copy()
        if basis == 1:  # For X-basis, apply H before measurement.
            measured_qc.h(0)
        measured_qc.measure(0, 0)
        measured_circuits.append(measured_qc)
    return measured_circuits

# Filter bits 
def remove_garbage(a_bases, b_bases, bits):
    return [bit for i, bit in enumerate(bits) if a_bases[i] == b_bases[i]]

# Create circuit 
def create_full_circuit(alice_bits, alice_bases, bob_bases):
    n_qubits = len(alice_bits)
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Alice's state preparation.
    for i in range(n_qubits):
        if alice_bases[i] == 0:  # Z-basis
            if alice_bits[i] == 1:
                qc.x(i)
        else:
            if alice_bits[i] == 0:
                qc.h(i)
            else:
                qc.x(i)
                qc.h(i)
    qc.barrier()
    
    # Bob's measurement
    for i in range(n_qubits):
        if bob_bases[i] == 1:
            qc.h(i)
    qc.measure_all()
    
    return qc

def bb84_protocol(n_bits=4, seed=0):
    np.random.seed(seed)
    
    # Alice's random bits and bases.
    alice_bits = QRNG(n_bits)
    alice_bases = QRNG(n_bits)
    
    # Circuits for each qubit.
    message = encode_message(alice_bits, alice_bases)
    
    # Bob's random measurement bases.
    bob_bases = QRNG(n_bits)
    bob_circuits = measure_message(message, bob_bases)
    
    # Full circuit
    full_circuit = create_full_circuit(alice_bits, alice_bases, bob_bases)
    
    
    service = QiskitRuntimeService(channel="ibm_quantum", instance="ibm-q/open/main")
    backend = service.least_busy(operational=True, simulator=False)
    
    # Run circuit
    sampler = Sampler(mode=backend)
    
    transpiled_circuits = transpile(bob_circuits, backend)
    
    # 1 shot per circuit.
    job = sampler.run(transpiled_circuits, shots=1)
    result = job.result()
    
    # Extract measurement outcomes.
    counts_list = [res.data.c.get_counts() for res in result]
    bob_measured_bits = [int(list(count.keys())[0], 2) for count in counts_list]
    
    # Generate sifted keys by comparing bases.
    alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
    bob_key = remove_garbage(alice_bases, bob_bases, bob_measured_bits)
    
    mismatched_bits = 0
    for( a_bit, b_bit ) in zip(alice_key, bob_key):
        if a_bit != b_bit:
            mismatched_bits += 1
    
    return {
        'alice_bits': alice_bits,
        'alice_bases': alice_bases,
        'bob_bases': bob_bases,
        'bob_results': bob_measured_bits,
        'alice_key': alice_key,
        'bob_key': bob_key,
        'job_id': job.job_id(),
        'full_circuit': full_circuit,
        'mismatched_bits': mismatched_bits
    }

def analyze_results(results):
    print("Initial values:")
    print(f"Alice's bits: {results['alice_bits']}")
    print(f"Alice's bases: {results['alice_bases']}")
    print(f"Bob's bases: {results['bob_bases']}")
    print(f"Bob's results: {results['bob_results']}")
    print("\nGenerated keys:")
    print(f"Alice's key: {results['alice_key']}")
    print(f"Bob's key: {results['bob_key']}")
    print(f"QBER: {results['mismatched_bits']} / {len(results['alice_key'])} = {results['mismatched_bits'] / len(results['alice_key']):.2%}")
    print(f"Key Rate: {len(results['alice_key']) / len(results['alice_bits']):.2%}")
    
    if results['alice_key'] == results['bob_key']:
        print("\nSuccess: Keys match!")
    else:
        print("\nWarning: Keys do not match")
        for i, (a, b) in enumerate(zip(results['alice_key'], results['bob_key'])):
            if a != b:
                print(f"Position {i}: Alice has {a}, Bob has {b}")
        errors = sum(a != b for a, b in zip(results['alice_key'], results['bob_key']))
        qber = errors / len(results['alice_key']) if results['alice_key'] else 0
        print(f"\nQuantum Bit Error Rate (QBER): {qber:.2%}")
    
    print(f"\nJob ID: {results['job_id']}")
    print("\nFull Circuit Diagram:")
    print(results['full_circuit'])

if __name__ == "__main__":
    try:
        print("Executing BB84 protocol on ibm_kyiv using Qiskit Runtime primitives...")
        results = bb84_protocol(n_bits=5)
        analyze_results(results)
    except Exception as e:
        print(f"Error during execution: {str(e)}")
