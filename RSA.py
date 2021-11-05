from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

class RSAService:
    @staticmethod
    def encrypt(key, plainText):
        plainText = str.encode(plainText)
        key = RSA.importKey(key)
        cipher = PKCS1_OAEP.new(key)
        ciphertext = cipher.encrypt(plainText)
        return str(base64.b64encode(ciphertext), 'utf-8')

    @staticmethod
    def decrypt(key, encryptedText):
        key = RSA.importKey(key)
        cipher = PKCS1_OAEP.new(key)
        return str(cipher.decrypt(base64.b64decode(encryptedText)), 'utf-8')


if __name__ == "__main__":
    encryptedText = RSAService.encrypt(open('./public.pem').read(), 'hello world')
    decryptedText = RSAService.decrypt(open('./private.pem').read(), encryptedText)
    print(encryptedText)
    print(decryptedText)