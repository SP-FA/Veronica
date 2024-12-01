from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64


def encode_by_public_key(plain, pemPublicKey):
    publicKey = serialization.load_pem_public_key(pemPublicKey)
    plainBytes = plain.encode('utf-8')

    cipherText = publicKey.encrypt(plainBytes, padding.PKCS1v15())
    cipherBase64 = base64.b64encode(cipherText)
    return cipherBase64.decode()


def update_encoded_credentials(pemPath, cfg):
    account = cfg['mw']['account']
    pwd = cfg['mw']['password']

    with open(pemPath, "rb") as keyFile:
        pemPublicKey = keyFile.read()

    encodeAccount = encode_by_public_key(account, pemPublicKey)
    encodePwd = encode_by_public_key(pwd, pemPublicKey)

    cfg.set('credentials', 'account', encodeAccount)
    cfg.set('credentials', 'password', encodePwd)
    return cfg
