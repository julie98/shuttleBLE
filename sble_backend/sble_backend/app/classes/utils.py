import hashlib


class Utils(object):
    @staticmethod
    def create_id(hash_str):
        m = hashlib.sha256()
        m.update(bytes(hash_str, 'utf-8'))
        return m.hexdigest()
