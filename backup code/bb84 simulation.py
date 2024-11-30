import random

def threshold_error_rate():
    """Calculates the theoretical threshold error rate for secure BB84"""
    return 0.146  # Secure threshold for BB84 protocol

def generate_basis(num_bits):
    """Generates a random list of basis choices (rectilinear or diagonal)"""
    return [random.choice(['R', 'D']) for _ in range(num_bits)]

def encode_qubit(basis, bit):
    """Encodes a classical bit based on the chosen basis"""
    if basis == 'R':
        return 'H' if bit else 'V'
    else:
        return '+' if bit else 'X'

def decode_qubit(basis, state):
    """Decodes a received quantum state based on the chosen basis"""
    if basis == 'R':
        return 1 if state == 'H' else 0
    else:
        return 1 if state == '+' else 0

def simulate_noise(state, error_rate):
    """Simulates noise on the quantum channel"""
    if random.random() < error_rate:
        return random.choice(['H', 'V', '+', 'X'])
    else:
        return state

def eavesdrop(encoded_qubits):
    """Simulates Eve's intercept-resend attack"""
    eve_basis = [random.choice(['R', 'D']) for _ in range(len(encoded_qubits))]
    eve_measurements = [decode_qubit(b, state) for b, state in zip(eve_basis, encoded_qubits)]
    eve_states = [encode_qubit(b, m) for b, m in zip(eve_basis, eve_measurements)]
    return eve_states, eve_measurements

def main():
    # Get user input
    num_bits = int(input("Enter number of bits to transfer: "))

    # Calculate channel error rate based on security threshold
    q = threshold_error_rate()

    # Alice generates random bits and basis choices
    alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
    alice_basis = generate_basis(num_bits)

    # Encode qubits
    encoded_qubits = [encode_qubit(b, a) for b, a in zip(alice_basis, alice_bits)]

    # Simulate Eve's attack
    eve_states, eve_measurements = eavesdrop(encoded_qubits)

    # Simulate noisy channel
    received_qubits = []
    noise_count = 0
    for state in eve_states:
        noisy_state = simulate_noise(state, q)
        if noisy_state != state:
            noise_count += 1
        received_qubits.append(noisy_state)

    # Bob generates his own basis choices
    bob_basis = generate_basis(num_bits)

    # Bob decodes qubits based on his guessed basis
    bob_bits = [decode_qubit(b, state) for b, state in zip(bob_basis, received_qubits)]

    # Public channel for basis comparison
    matching_indices = [i for i in range(num_bits) if alice_basis[i] == bob_basis[i]]
    alice_matching_bits = [alice_bits[i] for i in matching_indices]
    bob_matching_bits = [bob_bits[i] for i in matching_indices]

    # Sifted key after basis comparison
    sifted_key = alice_matching_bits

    # Calculate the error rate due to Eve's attack
    eve_errors = sum(1 for i in matching_indices if alice_bits[i] != eve_measurements[i])
    e = eve_errors / len(matching_indices) if matching_indices else 0

    # Calculate Bit Error Rate (BER)
    ber = q + (1 - q) * e / 2

    # Estimate Eve's success rate (heuristic based on errors in matched basis)
    eve_success_rate_estimate = eve_errors / len(matching_indices) if matching_indices else 0

    # Calculate Noise Level
    noise_level = noise_count / num_bits

    # Print results
    print("Protocol Type: BB84")
    print("Protocol Parameters: Number of Basis Choices: 2 (Rectilinear or Diagonal)")
    print("Alice's Bits: ", alice_bits)
    print("Alice's Basis: ", alice_basis)
    print("Bob's Basis: ", bob_basis)
    print("Bob's Bits: ", bob_bits)
    print("Sifted Key: ", sifted_key)
    print("Bit Error Rate (BER): ", ber)
    print("Eve's Success Rate Estimate: ", eve_success_rate_estimate)
    print("Noise Level: ", noise_level)

if __name__ == "__main__":
    main()
