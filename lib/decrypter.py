import base64
import hmac
import binascii
import datetime
import struct
import realtime_bidding_pb2
import hyperlocal_pb2
from hashlib import sha1


class DecrypterException(Exception):
    pass


class Secret(object):
    def __init__(self, encryption_encoded_key, integrity_encoded_key):
        self.encryption_key = self._urlsafe_b64decode(encryption_encoded_key)
        self.integrity_key = self._urlsafe_b64decode(integrity_encoded_key)

    def _urlsafe_b64decode(self, s):
        return base64.urlsafe_b64decode(s + '=' * (4 - len(s) % 4))


class Decrypter(object):
    def __init__(self, secret, iv_length, is_length, byte_length):
        self.encryption_key = secret.encryption_key
        self.integrity_key = secret.integrity_key
        self.iv_length = iv_length
        self.is_length = is_length
        self.byte_length = byte_length

    def run(self, long_ciphertext):
        initialization_vector, ciphertext, integrity_signature = \
            self._parse_long_ciphertext(long_ciphertext)

        plaintext = self._get_plaintext(ciphertext, initialization_vector)
        date = self._get_date(initialization_vector)

        if not self._check_signature(
                plaintext, initialization_vector, integrity_signature):
            raise DecrypterException('Invalid signature')

        return {'plaintext': plaintext, 'datetime': date}

    def deserialize_bid_request(self, serialized_protocol_buffer):
        bid_request = realtime_bidding_pb2.BidRequest()
        bid_request.ParseFromString(serialized_protocol_buffer)
        return bid_request

    def _parse_long_ciphertext(self, long_ciphertext):
        initialization_vector = long_ciphertext[0:  self.iv_length]
        ciphertext = long_ciphertext[self.iv_length: -self.is_length]
        integrity_signature = long_ciphertext[-self.is_length:]
        return initialization_vector, ciphertext, integrity_signature

    def _get_plaintext(self, ciphertext, iv):
        plaintext = []
        add_iv_counter_byte = True
        n = 0

        while len(ciphertext) > n * self.byte_length:
            data = ciphertext[n * self.byte_length: (n + 1) * self.byte_length]
            pad = hmac.new(self.encryption_key, iv, sha1).hexdigest()
            pad = binascii.unhexlify(pad)
            byte_array = struct.unpack(str(len(data)) + 'B', data)
            pad = struct.unpack('20B', pad)

            for key in range(len(byte_array)):
                plaintext.append(chr(byte_array[key] ^ pad[key]))

            if not add_iv_counter_byte:
                if n % 256 == 0:
                    add_iv_counter_byte = True
                iv = self._add_initialization_vector(iv)

            if add_iv_counter_byte:
                add_iv_counter_byte = False
                iv += '\x00'
            n += 1
        return ''.join(plaintext)

    def _check_signature(self, plaintext, initialization_vector,
                         integrity_signature):
        hex_signature = hmac.new(self.integrity_key,
                                 plaintext + initialization_vector,
                                 sha1).hexdigest()
        signature = binascii.unhexlify(hex_signature)
        computed_signature = signature[0: self.is_length]
        return computed_signature == integrity_signature

    def _add_initialization_vector(self, iv):
        array = struct.unpack(str(len(iv)) + 'c', iv)
        result = []
        for key in range(len(array)):
            value = array[key]
            if len(array) - 1 == key:
                bin_value = struct.pack('h', int(binascii.hexlify(value)) + 1)
                value = struct.unpack(str(len(bin_value)) + 'c', bin_value)[0]
            result.append(struct.pack('c', value))
        return ''.join(result)

    def _get_date(self, iv):
        sec = struct.unpack('>i', iv[0: 4])
        usec = struct.unpack('>i', iv[4: 8])
        timestamp = sec[0] + usec[0] / 1000
        return datetime.datetime.fromtimestamp(timestamp).strftime(
            '%Y/%m/%d %H:%M:%S')


class DecrypterHyperLocal(Decrypter):
    iv_length = 16
    is_length = 4
    byte_length = 20

    def __init__(self, encryption_encoded_key, integrity_encoded_key):
        secret = Secret(encryption_encoded_key, integrity_encoded_key)
        super(DecrypterHyperLocal, self).__init__(
            secret, self.iv_length, self.is_length, self.byte_length)

    def decryption(self, long_ciphertext):
        result = super(DecrypterHyperLocal, self).run(long_ciphertext)
        hyper_local = self._decrypt_hyper_local(result['plaintext'])

        return {'hyperlocal': hyper_local, 'datetime': result['datetime']}

    def _decrypt_hyper_local(self, plaintext):
        hyper_local_set = hyperlocal_pb2.HyperlocalSet()
        hyper_local_set.ParseFromString(plaintext)
        corners = self._get_corners(hyper_local_set.hyperlocal)
        center = self._get_lat_long(hyper_local_set.center_point)

        return {'corners': corners, 'center_point': center}

    def _get_corners(self, hyper_local_set):
        corners = []
        for corner in hyper_local_set[0].corners:
            corners.append(self._get_lat_long(corner))
        return corners

    def _get_lat_long(self, point):
        return {'lat': point.latitude, 'long': point.longitude}


class DecrypterPrice(Decrypter):
    iv_length = 16
    is_length = 4
    byte_length = 8

    def __init__(self, encryption_encoded_key, integrity_encoded_key):
        secret = Secret(encryption_encoded_key, integrity_encoded_key)
        super(DecrypterPrice, self).__init__(
            secret, self.iv_length, self.is_length, self.byte_length)

    def decryption(self, long_ciphertext):
        result = super(DecrypterPrice, self).run(long_ciphertext)
        price = struct.unpack('>Q', result['plaintext'])
        return {'price': price[0], 'datetime': result['datetime']}


class DecrypterIdfa(Decrypter):
    iv_length = 16
    is_length = 4
    byte_length = 16

    def __init__(self, encryption_encoded_key, integrity_encoded_key):
        secret = Secret(encryption_encoded_key, integrity_encoded_key)
        super(DecrypterIdfa, self).__init__(
            secret, self.iv_length, self.is_length, self.byte_length)

    def decryption(self, long_ciphertext):
        result = super(DecrypterIdfa, self).run(long_ciphertext)
        return {'idfa': result['plaintext'], 'datetime': result['datetime']}