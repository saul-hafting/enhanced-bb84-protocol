# Setup Guide for Enhanced BB84 Protocol

This guide will help you set up and run the Enhanced BB84 Quantum Key Distribution protocol on your local machine.

## 📋 Prerequisites

### IBM Quantum Account

You'll need a free IBM Quantum account to access quantum hardware.

1. Go to [IBM Quantum Experience](https://quantum-computing.ibm.com/)
2. Create a free account or sign in
3. Navigate to "Account Settings" → "API Token"
4. Copy your API token (you'll need this later)

## 🔧 Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/enhanced-bb84-protocol.git
cd enhanced-bb84-protocol
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv quantum_env

# Activate virtual environment
# On Windows:
source quantum_env/Scripts/activate
# On macOS/Linux:
source quantum_env/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure IBM Quantum Access

1. Open `main.py` in your text editor
2. Find this line:

   ```python
   token="YOUR_API_TOKEN_HERE",
   ```

3. Replace `YOUR_API_TOKEN_HERE` with your actual IBM Quantum API token
4. Save the file

## 🚀 Running the Protocol

### Basic Execution

```bash
python main.py
```

## 🔍 Understanding the Results

### Key Metrics Explained

**QBER (Quantum Bit Error Rate)**

- Measures the percentage of mismatched bits in the final key
- 0% = Perfect (ideal scenario)
- < 11% = Secure communication possible
- \> 11% = Potential eavesdropping or high noise

**Key Generation Rate**

- Percentage of transmitted qubits that become usable key bits
- Typically ~50% due to random basis matching
- Higher rates indicate better efficiency
