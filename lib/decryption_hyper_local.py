import hyperlocal_pb2
import decryption


class DecrypterHyperLocal(decryption.Decrypter):
    iv_length = 16
    is_length = 4
    byte_length = 20

    def __init__(self, encryption_encoded_key, integrity_encoded_key):
        super(DecrypterHyperLocal, self).__init__(
            encryption_encoded_key, integrity_encoded_key,
            self.iv_length, self.is_length, self.byte_length)

    def decryption(self, long_ciphertext):
        result = super(DecrypterHyperLocal, self).run(long_ciphertext)
        hyper_local = self.decrypt_hyper_local(result['plaintext'])

        return {'hyperlocal': hyper_local, 'datetime': result['datetime']}

    def decrypt_hyper_local(self, plaintext):
        hyper_local_set = hyperlocal_pb2.HyperlocalSet()
        hyper_local_set.ParseFromString(plaintext)
        corners = self.get_corners(hyper_local_set.hyperlocal)
        center = self.get_lat_long(hyper_local_set.center_point)

        return {'corners': corners, 'center_point': center}

    def get_corners(self, hyper_local_set):
        corners = []
        for corner in hyper_local_set[0].corners:
            corners.append(self.get_lat_long(corner))
        return corners

    def get_lat_long(self, point):
        return {'lat': point.latitude, 'long': point.longitude}
