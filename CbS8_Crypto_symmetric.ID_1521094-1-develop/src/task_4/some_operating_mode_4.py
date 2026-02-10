class YetAnotherMode(CustomBlockCipher):
    def __init__(self, key, iv):
        super().__init__(key)
        self.iv = iv

    def encrypt(self, plaintext):
        plaintext = self._pad(plaintext)
        ciphertext = b""
        feedback = self.iv
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            feedback = self._xor_block(feedback, self.key)
            cipher_feedback = self._xor_block(block, feedback)
            ciphertext += cipher_feedback
        return ciphertext

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)
