class AnotherMode(CustomBlockCipher):
    def __init__(self, key, iv):
        super().__init__(key)
        self.iv = iv

    def encrypt(self, plaintext):
        plaintext = self._pad(plaintext)
        ciphertext = b""
        previous_block = self.iv
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            encrypted_block = self._xor_block(previous_block, self.key)
            cipher_feedback = self._xor_block(block, encrypted_block)
            ciphertext += cipher_feedback
            previous_block = cipher_feedback
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b""
        previous_block = self.iv
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            encrypted_block = self._xor_block(previous_block, self.key)
            decrypted_block = self._xor_block(block, encrypted_block)
            plaintext += decrypted_block
            previous_block = block
        return self._unpad(plaintext)
