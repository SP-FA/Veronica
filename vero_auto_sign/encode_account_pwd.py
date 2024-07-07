from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import configparser


def encode(plain, pemPublicKey):
    publicKey = serialization.load_pem_public_key(pemPublicKey)
    plainBytes = plain.encode('utf-8')

    cipherText = publicKey.encrypt(plainBytes, padding.PKCS1v15())
    cipherBase64 = base64.b64encode(cipherText)
    return cipherBase64.decode()


def get_encode(pemPath, cfg):
    account = cfg['mw']['account']
    pwd = cfg['mw']['password']

    with open(pemPath, "rb") as keyFile:
        pemPublicKey = keyFile.read()

    encodeAccount = encode(account, pemPublicKey)
    encodePwd = encode(pwd, pemPublicKey)

    cfg.set('credentials', 'account', encodeAccount)
    cfg.set('credentials', 'password', encodePwd)
    return cfg
