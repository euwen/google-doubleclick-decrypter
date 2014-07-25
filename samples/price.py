import sys
import base64
sys.path.insert(0, '../lib')
from decrypter import DecrypterPrice

encryption_encoded_key = 'sIxwz7yw62yrfoLGt12lIHKuYrK_S5kLuApI2BQe7Ac'
integrity_encoded_key = 'v3fsVcMBMMHYzRhi7SpM0sdqwzvAxM6KPTu9OtVod5I'
long_ciphertext = 'SjpvRwAB4kB7jEpgW5IA8p73ew9ic6VZpFsPnA'
safe_long_ciphertext = base64.urlsafe_b64decode(
    long_ciphertext + '=' * (4 - len(long_ciphertext) % 4))

decrypt_price = DecrypterPrice(encryption_encoded_key, integrity_encoded_key)
print decrypt_price.decryption(safe_long_ciphertext)