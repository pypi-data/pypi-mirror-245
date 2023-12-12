# rsa_code.py

def generate_keypair():
    # Your RSA code here
    import sympy

    def generate_keypair():
        p = sympy.randprime(100, 1000)
        q = sympy.randprime(100, 1000)
        n = p * q
        phi_n = (p - 1) * (q - 1)
        e = sympy.randprime(2, phi_n - 1)
        d = sympy.mod_inverse(e, phi_n)
        return ((n, e), (n, d))

    def encrypt(number, public_key):
        n, e = public_key
        ciphertext = pow(number, e, n)
        return ciphertext

    def decrypt(ciphertext, private_key):
        n, d = private_key
        decrypted_number = pow(ciphertext, d, n)
        return decrypted_number

    # Example usage:
    public_key, private_key = generate_keypair()
    original_number = 42
    encrypted_number = encrypt(original_number, public_key)
    decrypted_number = decrypt(encrypted_number, private_key)

    print(f"Original number: {original_number}")
    print(f"Encrypted number: {encrypted_number}")
    print(f"Decrypted number: {decrypted_number}")

    pass
