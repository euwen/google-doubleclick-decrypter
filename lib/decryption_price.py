import decryption
import struct


class DecrypterPrice(decryption.Decrypter):
    iv_length = 16
    is_length = 4
    byte_length = 8

    def __init__(self, encryption_encoded_key, integrity_encoded_key):
        super(DecrypterPrice, self).__init__(
            encryption_encoded_key, integrity_encoded_key,
            self.iv_length, self.is_length, self.byte_length)

    def decryption(self, long_ciphertext):
        result = super(DecrypterPrice, self).run(long_ciphertext)
        price = struct.unpack(">Q", result["plaintext"])
        return {'price': price[0], 'datetime': result["datetime"]}
