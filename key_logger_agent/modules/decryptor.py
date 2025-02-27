import os
from .encryption import XorEncryption

class Decryptor:
    def __init__(self, encrypted_file_path: str, xor_key: str):
        """
        When called by the server, this class will process an encrypted file
        and decrypt its contents using the given XOR key.
        """
        self.encrypted_file_path = encrypted_file_path
        self.xor_key = xor_key
        self.xor_cipher = XorEncryption()  # Using XorEncryption to maintain compatibility

    def decrypt(self) -> str:
        """
        Reads the encrypted file and decrypts its contents.

        Initially, we thought decryption should be handled within the Encryption class,
        but it turns out we only need it here.

        The main question was whether to initialize the class variables (`self.encrypted_file_path` and `self.xor_key`)
        or pass them directly as method arguments, but for now, this approach works fine.
        """
        if not os.path.exists(self.encrypted_file_path):
            raise FileNotFoundError(f"The file {self.encrypted_file_path} was not found!")

        try:
            with open(self.encrypted_file_path, "r", encoding="utf-8") as f:
                encrypted_data = f.read().strip()  # Reading as text (since encryption outputs hex)

            # Decrypt using the same XorEncryption logic
            decrypted_data = self.xor_cipher.decryption(encrypted_data, self.xor_key)
            return decrypted_data
        except Exception as e:
            raise RuntimeError(f"Error while decrypting the file: {e}")

# Example usage
if __name__ == "__main__":
    decryptor = Decryptor("encrypted_file.txt", "מפתח")
    try:
        decrypted_text = decryptor.decrypt()
        print(f"Decrypted text: {decrypted_text}")
    except Exception as e:
        print(f"Error: {e}")
