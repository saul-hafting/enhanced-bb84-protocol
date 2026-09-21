# Enhanced BB84 Quantum Key Distribution Protocol

An improved implementation of the BB84 Quantum Key Distribution (QKD) protocol using Qiskit and IBM Quantum hardware, featuring **true quantum random number generation** for enhanced security.

## 🚀 Key Improvements

This implementation enhances the original BB84 protocol by incorporating:

- **Quantum Random Number Generator (QRNG)**: Uses quantum superposition and measurement to generate truly random bits and bases
- **Real IBM Quantum Hardware**: Executes on actual quantum computers rather than simulators
- **Comprehensive Metrics**: Calculates Quantum Bit Error Rate (QBER) and Key Generation Rate
- **Automatic Backend Selection**: Dynamically selects the least busy quantum backend

## 🔬 How It Works

### Original vs Enhanced Implementation

**Original**: Used pseudo-random number generation (`np.random`) for Alice and Bob's bits and bases.

**Enhanced**: Implements true quantum randomness through superposition states:

```python
def QRNG(n_bits):
    circuit = QuantumCircuit(n_bits, n_bits)
    circuit.h(range(n_bits))  # Create superposition
    circuit.measure(range(n_bits), range(n_bits))  # Collapse to random state
    # Execute on real quantum hardware...
```

### Protocol Flow

1. **Quantum Random Generation**: Alice and Bob's bits and bases are generated using quantum superposition
2. **State Preparation**: Alice encodes her random bits using random bases (Z or X basis)
3. **Transmission & Measurement**: Bob measures the qubits using his random bases
4. **Basis Reconciliation**: Only measurements where Alice and Bob used the same basis are kept
5. **Key Generation**: The sifted bits form the shared cryptographic key

## 📋 Prerequisites

- Python 3.9+
- IBM Quantum account and API token
- Required Python packages (see `requirements.txt`)

## 🛠️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/saul-hafting/enhanced-bb84-protocol.git
   cd enhanced-bb84-protocol
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up IBM Quantum credentials:**
   - Get your API token from [IBM Quantum Experience](https://quantum-computing.ibm.com/)
   - Replace the token in `main.py` with your actual API key:

   ```python
   QiskitRuntimeService.save_account(
       token="YOUR_API_TOKEN_HERE",
       channel="ibm_quantum",
       overwrite=True
   )
   ```

## 🚀 Usage

Run the enhanced BB84 protocol:

```bash
python main.py
```

### Sample Output

```
Executing BB84 protocol using Qiskit Runtime primitives...

Initial values:
Alice's bits: [1, 0, 1, 0, 1]
Alice's bases: [0, 1, 0, 1, 0]
Bob's bases: [0, 0, 0, 1, 1]
Bob's results: [1, 1, 1, 0, 0]

Generated keys:
Alice's key: [1, 1, 0]
Bob's key: [1, 1, 0]
QBER: 0 / 3 = 0.00%
Key Rate: 60.00%

Success: Keys match!

Job ID: ch91x2v4d6sg008wmr4g

Full Circuit Diagram:
        ┌───┐ ░ ┌───┐ ░ ┌─┐
   q_0: ┤ H ├─░─┤ H ├─░─┤M├────────────
        ├───┤ ░ └───┘ ░ └╥┘┌─┐
   q_1: ┤ X ├─░───────░──╫─┤M├─────────
        ├───┤ ░       ░  ║ └╥┘┌─┐
   q_2: ┤ X ├─░───────░──╫──╫─┤M├──────
        ├───┤ ░ ┌───┐ ░  ║  ║ └╥┘┌─┐
   q_3: ┤ X ├─░─┤ H ├─░──╫──╫──╫─┤M├───
        ├───┤ ░ └───┘ ░  ║  ║  ║ └╥┘┌─┐
   q_4: ┤ X ├─░───────░──╫──╫──╫──╫─┤M├
        └───┘ ░       ░  ║  ║  ║  ║ └╥┘
   c: 5/═════════════════╬══╬══╬══╬══╬═
                         ║  ║  ║  ║  ║
meas: 5/═════════════════╩══╩══╩══╩══╩═
                         0  1  2  3  4
```

## 📊 Performance Metrics

The implementation provides two key security metrics:

### Quantum Bit Error Rate (QBER)

- **Formula**: `(Mismatched bits) / (Total sifted key length)`
- **Ideal**: 0% (perfect key agreement)
- **Acceptable**: < 11% for secure communication

### Key Generation Rate

- **Formula**: `(Sifted key length) / (Total transmitted qubits)`
- **Typical**: ~50% (due to random basis matching)
- **Factors**: Basis correlation, quantum noise, eavesdropping

## 🎯 Use Cases

- **Quantum Cryptography Research**: Study QKD protocols and security
- **Educational Purposes**: Learn quantum information concepts
- **Proof of Concept**: Demonstrate quantum-secured communication
- **Benchmarking**: Test quantum hardware capabilities

## ⚠️ Important Notes

- **Quantum Credits**: Running on real hardware consumes quantum credits
- **Network Latency**: Results may take time due to quantum job queuing

## 🙏 Acknowledgments

- Original implementation from [codeocean.com](https://codeocean.com/capsule/8352553/tree/v1)

## License

This project is a modified version of a BB84 implementation originally
from codeocean.com, licensed under the GNU General Public License v3.0,
and is therefore distributed under the **GPLv3**. See the LICENSE file.

Modifications by Saul Hafting: quantum random number generation (QRNG)
and related changes.
