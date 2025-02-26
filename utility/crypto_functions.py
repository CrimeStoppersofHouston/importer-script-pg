'''
    This file should contain all of the functions needed to
    encrypt and decrypt data for insertions
'''

### External Imports ###

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

### Function Declarations ###

def encrypt_AES(data, key, iv, padding_style='pkcs7') -> bytes:
    data = str(data).encode()

    cipher = AES.new(key, AES.MODE_CBC, iv)

    padded_data = pad(data, AES.block_size, padding_style)

    return cipher.encrypt(padded_data)

def bytes_to_hex_text(byte_object: bytes) -> str:
    '''
        This function converts the bytes object to hex and then
        encodes the hex values into utf-8 text for insertion
    '''
    return byte_object.hex().encode().decode()

def decrypt_AES(data, key, iv, padding_style='pkcs7') -> str:
    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted_data = cipher.decrypt(data)

    return unpad(decrypted_data, AES.block_size, padding_style).decode()

def hex_text_to_bytes(hex_text: str) -> bytes:
    '''
        This function converts the bytes object to hex and then
        encodes the hex values into utf-8 text for insertion
    '''
    return bytes.fromhex(hex_text)