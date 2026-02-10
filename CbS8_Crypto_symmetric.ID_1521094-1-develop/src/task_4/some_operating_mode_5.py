class LastMode(CustomBlockCipher):
    def __init__(self, key, iv):
        super().__init__(key)
        self.counter = iv

    def encrypt(self, plaintext):
        plaintext = self._pad(plaintext)
        ciphertext = b""
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            encrypted_counter = self._xor_block(self.counter, self.key)
            cipher_feedback = self._xor_block(block, encrypted_counter)
            ciphertext += cipher_feedback
            self.counter = self._increment(self.counter)
        return ciphertext

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)

    def _increment(self, param):
        value_as_int = int.from_bytes(param, byteorder='big')
        value_as_int += 1
        return value_as_int.to_bytes(self.block_size, byteorder='big')
