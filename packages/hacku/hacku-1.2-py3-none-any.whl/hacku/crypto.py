# coding=utf-8

import base64

import rsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def rsa_encrypt(msg, pub_key):
    public_key = f'-----BEGIN PUBLIC KEY-----\n{pub_key}\n-----END PUBLIC KEY-----'
    p_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key.encode())
    crypt_msg = rsa.encrypt(msg.encode(), p_key)
    return base64.b64encode(crypt_msg).decode()

def aes_enc(key, plaintext: str):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode(), AES.block_size, style='pkcs7')
    ciphertext = cipher.encrypt(padded_plaintext)
    return base64.b64encode(ciphertext).decode()