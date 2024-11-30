import random

def threshold_error_rate():
    """Calculates the theoretical threshold error rate for secure B92"""
    return 0.146  # Secure threshold for B92 protocol

def generate_basis(num_bits):
    """Generates a random list of basis choices (rectilinear or diagonal)"""
    return [random.choice(['R', 'D']) for _ in range(num_bits)]

def encode_qubit(bit):
    """Encodes a classical bit based on the chosen basis in B92 protocol"""
    return 'H' if bit else '+'

def decode_qubit(basis, state):
    """Decodes a received quantum state based on the chosen basis"""
    if basis == 'R':
        return 1 if state == 'H' else 0
    else:
        return 1 if state == '+' else 0

def simulate_noise(state, error_rate):
    """Simulates noise on the quantum channel"""
    if random.random() < error_rate:
        return random.choice(['H', '+'])
    else:
        return state

def eavesdrop(encoded_qubits, attack_type):
    """Simulates Eve's attack: Intercept-Resend Attack (IRA) or Phishing Attack (PA)"""
    if attack_type == 'IRA':
        eve_basis = generate_basis(len(encoded_qubits))
        eve_measurements = [decode_qubit(b, state) for b, state in zip(eve_basis, encoded_qubits)]
        eve_states = [encode_qubit(m) for m in eve_measurements]
    elif attack_type == 'PA':
        eve_states = ['H' if random.random() < 0.5 else '+' for _ in encoded_qubits]
        eve_measurements = [1 if state == 'H' else 0 for state in eve_states]
        eve_basis = ['R' if state == 'H' else 'D' for state in eve_states]
    return eve_states, eve_measurements, eve_basis

def main():
    # Get user input
    num_bits = int(input("Enter number of bits to transfer: "))
    attack_type = input("Enter Eve's attack type (IRA/PA): ")

    # Calculate channel error rate based on security threshold
    q = threshold_error_rate()

    # Alice generates random bits
    alice_bits = [random.randint(0, 1) for _ in range(num_bits)]

    # Encode qubits
    encoded_qubits = [encode_qubit(bit) for bit in alice_bits]

    # Simulate Eve's attack
    eve_states, eve_measurements, eve_basis = eavesdrop(encoded_qubits, attack_type)

    # Simulate noisy channel separately from Eve's attack
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
    matching_indices = [i for i in range(num_bits) if bob_basis[i] == ('R' if received_qubits[i] == 'H' else 'D')]
    alice_matching_bits = [alice_bits[i] for i in matching_indices]
    bob_matching_bits = [bob_bits[i] for i in matching_indices]

    # Sifted key after basis comparison
    sifted_key = alice_matching_bits

    # Calculate the error rate due to Eve's attack
    if attack_type == 'IRA':
        eve_matching_indices = [i for i in range(num_bits) if eve_basis[i] == ('R' if encoded_qubits[i] == 'H' else 'D')]
        eve_matching_bits = [eve_measurements[i] for i in eve_matching_indices]
        alice_eve_matching_bits = [alice_bits[i] for i in eve_matching_indices]
    elif attack_type == 'PA':
        eve_matching_indices = matching_indices
        eve_matching_bits = [eve_measurements[i] for i in eve_matching_indices]
        alice_eve_matching_bits = [alice_bits[i] for i in eve_matching_indices]

    eve_errors = sum(a != e for a, e in zip(alice_eve_matching_bits, eve_matching_bits))
    e = eve_errors / len(eve_matching_indices) if eve_matching_indices else 0

    # Calculate Bit Error Rate (BER)
    ber = q + (1 - q) * e / 2

    # Calculate Noise Level
    noise_level = noise_count / num_bits

    # Estimate Eve's success rate
    eve_success_rate_estimate = eve_errors / len(eve_matching_indices) if eve_matching_indices else 0

    # Print results
    print("Protocol Type: B92")
    print("Protocol Parameters: One basis choice: Rectilinear (R)")
    print("Alice's Bits: ", alice_bits)
    print("Bob's Basis: ", bob_basis)
    print("Bob's Bits: ", bob_bits)
    print("Sifted Key: ", sifted_key)
    print("Bit Error Rate (BER): ", ber)
    print("Eve's Success Rate Estimate: ", eve_success_rate_estimate)
    print("Noise Level: ", noise_level)
    print("Eve's Attack Type: ", attack_type)

if __name__ == "__main__":
    main()
