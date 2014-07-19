import decryption


class DecrypterIdfa(decryption.Decrypter):
    iv_length = 16
    is_length = 4
    byte_length = 16

    def __init__(self, encryption_encoded_key, integrity_encoded_key):
        super(DecrypterIdfa, self).__init__(
            encryption_encoded_key, integrity_encoded_key,
            self.iv_length, self.is_length, self.byte_length)

    def decryption(self, long_ciphertext):
        result = super(DecrypterIdfa, self).run(long_ciphertext)
        return {'idfa': result['plaintext'], 'datetime': result['datetime']}
