class SomeOtherMode(CustomBlockCipher):
    def __init__(self, key, iv):
        super().__init__(key)
        self.iv = iv

    def encrypt(self, plaintext):
        plaintext = self._pad(plaintext)
        ciphertext = b""
        previous_block = self.iv
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            block_to_encrypt = self._xor_block(block, previous_block)
            encrypted_block = self._xor_block(block_to_encrypt, self.key)
            ciphertext += encrypted_block
            previous_block = encrypted_block
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b""
        previous_block = self.iv
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            decrypted_block = self._xor_block(block, self.key)
            decrypted_block = self._xor_block(decrypted_block, previous_block)
            plaintext += decrypted_block
            previous_block = block
        return self._unpad(plaintext)
