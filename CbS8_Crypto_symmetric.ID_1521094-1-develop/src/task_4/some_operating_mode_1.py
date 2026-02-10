class SomeMode(CustomBlockCipher):
    def encrypt(self, plaintext):
        plaintext = self._pad(plaintext)
        ciphertext = b""
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            encrypted_block = self._xor_block(block, self.key)
            ciphertext += encrypted_block
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b""
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            decrypted_block = self._xor_block(block, self.key)
            plaintext += decrypted_block
        return self._unpad(plaintext)