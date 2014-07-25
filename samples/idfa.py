import sys
import binascii
sys.path.insert(0, '../lib')
from decrypter import DecrypterIdfa

encryption_encoded_key = 'AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8,'
integrity_encoded_key = 'Hx4dHBsaGRgXFhUUExIREA8ODQwLCgkIBwYFBAMCAQA,'

encrypted_hashed_idfa = binascii.unhexlify(
    '51928A6600000000AAAAAACEAAAAAACEB30E'
    'DBA1D938ACFB12C91670AB8D01F31E434557')
encrypted_advertising_id = binascii.unhexlify(
    '51928A6600000000AAAAAACEAAAAAACED2C3'
    '2DF16B1658B8447591BE4BA853922C55ABAD')

long_ciphertext = {
    'encrypted_hashed_idfa': encrypted_hashed_idfa,
    'encrypted_advertising_id': encrypted_advertising_id
}

decrypter = DecrypterIdfa(encryption_encoded_key, integrity_encoded_key)
idfa_set = decrypter.decryption(long_ciphertext['encrypted_hashed_idfa'])

print {
    'idfa_hex': idfa_set['idfa_hex'],
    'datetime': idfa_set['datetime'],
}

idfa_set = decrypter.decryption(long_ciphertext['encrypted_advertising_id'])

print {
    'android_id_hex': idfa_set['idfa_hex'],
    'datetime': idfa_set['datetime'],
}
