import sys
import os
import unittest
import binascii
import base64
sys.path.insert(0, '../lib')
from decrypter import DecrypterHyperLocal
from decrypter import DecrypterIdfa
from decrypter import DecrypterPrice


os.environ['TZ'] = 'America/Toronto'


class DecrypterHyperLocalTest(unittest.TestCase):
    def test_decryption(self):
        encryption_key = 'Au6oPGwSEeELn4iWbO7DSQjrlG9-1uRBr0KzwPMhgUA.'
        integrity_key = 'v__sVcMBMMHYzRhi7SpM0sdqwzvAxM6KPTu9OtVod5I.'
        long_ciphertext = binascii.unhexlify(
            'E2014EA201246E6F6E636520736F7572636501414243C0ADF6B9B6AC17DA218FB'
            '50331EDB376701309CAAA01246E6F6E636520736F7572636501414243C09ED4EC'
            'F2DB7143A9341FDEFD125D96844E25C3C202466E6F6E636520736F75726365024'
            '14243517C16BAFADCFAB841DE3A8C617B2F20A1FB7F9EA3A3600256D68151C093'
            'C793B0116DB3D0B8BE9709304134EC9235A026844F276797')

        decrypter = DecrypterHyperLocal(encryption_key, integrity_key)
        bid_request = decrypter.deserialize_bid_request(long_ciphertext)
        hlocal_set = decrypter.decryption(bid_request.encrypted_hyperlocal_set)

        expected = {
            'hyperlocal': {
                'center_point': {'lat': 0, 'long': 0},
                'corners': [
                    {'lat': 100.0, 'long': 100.0},
                    {'lat': 200.0, 'long': -300.0},
                    {'lat': -400.0, 'long': 500.0},
                    {'lat': -600.0, 'long': -700.0}
                ]
            },
            'datetime': '2028/10/06 20:59:00'
        }
        self.assertEqual(hlocal_set, expected)


class DecrypterIdfaTest(unittest.TestCase):
    def test_idfa_decryption(self):
        encryption_key = 'AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8,'
        integrity_key = 'Hx4dHBsaGRgXFhUUExIREA8ODQwLCgkIBwYFBAMCAQA,'
        encrypted_hashed_idfa = binascii.unhexlify(
            '51928A6600000000AAAAAACEAAAAAACEB30E'
            'DBA1D938ACFB12C91670AB8D01F31E434557')

        decrypter = DecrypterIdfa(encryption_key, integrity_key)
        idfa_set = decrypter.decryption(encrypted_hashed_idfa)

        expected = {
            'idfa_bytes': ';fqT\xff\xa2\xbc:\xdf/A\x13cD\xaa\xee',
            'idfa_hex': '3b667154ffa2bc3adf2f41136344aaee',
            'datetime': '2013/05/14 15:03:02'
        }
        self.assertDictEqual(idfa_set, expected)

    def test_advertising_id_decryption(self):
        encryption_key = 'AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8,'
        integrity_key = 'Hx4dHBsaGRgXFhUUExIREA8ODQwLCgkIBwYFBAMCAQA,'
        encrypted_advertising_id = binascii.unhexlify(
            '51928A6600000000AAAAAACEAAAAAACED2C3'
            '2DF16B1658B8447591BE4BA853922C55ABAD')

        decrypter = DecrypterIdfa(encryption_key, integrity_key)
        idfa_set = decrypter.decryption(encrypted_advertising_id)

        expected = {
            'idfa_bytes': 'Z\xab\x87\x04M\x8cHy\x89\x93\xc6\xdd\x83a\xf8\x8f',
            'idfa_hex': '5aab87044d8c48798993c6dd8361f88f',
            'datetime': '2013/05/14 15:03:02'
        }
        self.assertDictEqual(idfa_set, expected)


class DecrypterPriceTest(unittest.TestCase):
    def test_price_decryption(self):
        encryption_key = 'sIxwz7yw62yrfoLGt12lIHKuYrK_S5kLuApI2BQe7Ac'
        integrity_key = 'v3fsVcMBMMHYzRhi7SpM0sdqwzvAxM6KPTu9OtVod5I'
        long_ciphertext = 'SjpvRwAB4kB7jEpgW5IA8p73ew9ic6VZpFsPnA'
        safe_long_ciphertext = base64.urlsafe_b64decode(
            long_ciphertext + '=' * (4 - len(long_ciphertext) % 4))

        decrypter = DecrypterPrice(encryption_key, integrity_key)
        price = decrypter.decryption(safe_long_ciphertext)

        expected = {'price': 709959680, 'datetime': '2009/06/18 12:48:02'}
        self.assertDictEqual(price, expected)
