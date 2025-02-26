'''
    Test suite for crypto methods
'''

import unittest
import os
from contextlib import closing

from utility.crypto_functions import (
    encrypt_AES,
    decrypt_AES,
    bytes_to_hex_text,
    hex_text_to_bytes
)

class TestCrypto(unittest.TestCase):
    
    def setUp(self):
        with closing(open('./tests/test_setups/crypto_files/test.key', 'rb')) as f:
            self.key = f.read()
        with closing(open('./tests/test_setups/crypto_files/test.iv', 'rb')) as f:
            self.iv = f.read()

    def test_encryption_process(self):
        target = 'Sample text unencrypted'

        encrypted = encrypt_AES(target, self.key, self.iv)
        self.assertIsInstance(encrypted, bytes)

        hex_text = bytes_to_hex_text(encrypted)
        self.assertIsInstance(hex_text, str)

        byte_obj = hex_text_to_bytes(hex_text)
        self.assertIsInstance(byte_obj, bytes)

        decrypted = decrypt_AES(byte_obj, self.key, self.iv)
        self.assertEqual(target, decrypted)