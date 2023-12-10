from Crypto.Cipher import PKCS1_OAEP, AES
from base64 import b64decode, b64encode
from Crypto.Signature import pkcs1_15
from json import dumps, JSONDecoder
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from secrets import choice
from re import findall


ASCII_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
ASCII_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Crypto:
    AES_IV = b'\x00' * 16

    @staticmethod
    def decode_auth(auth: str) -> str:
        """
        Decode an auth string by applying character substitutions.

        Args:
            auth (str): The input auth string.

        Returns:
            str: The decoded auth string.
        """
        result_list, digits = [], '0123456789'
        translation_table_lower = str.maketrans(
            ASCII_LOWERCASE,
            ''.join([chr(((32 - (ord(c) - 97)) % 26) + 97) for c in ASCII_LOWERCASE])
        )
        translation_table_upper = str.maketrans(
            ASCII_UPPERCASE,
            ''.join([chr(((29 - (ord(c) - 65)) % 26) + 65) for c in ASCII_UPPERCASE])
        )

        for char in auth:
            if char in ASCII_LOWERCASE:
                result_list.append(char.translate(translation_table_lower))
            elif char in ASCII_UPPERCASE:
                result_list.append(char.translate(translation_table_upper))
            elif char in digits:
                result_list.append(chr(((13 - (ord(char) - 48)) % 10) + 48))
            else:
                result_list.append(char)

        return ''.join(result_list)

    @classmethod
    def passphrase(cls, auth: str):
        """
        Generate a passphrase from an auth string.

        Args:
            auth (str): The input auth string.

        Returns:
            str: The generated passphrase.
        """
        if len(auth) != 32:
            raise ValueError('auth length should be 32 digits')

        result_list = []
        chunks = findall(r'\S{8}', auth)
        for character in (chunks[2] + chunks[0] + chunks[3] + chunks[1]):
            result_list.append(chr(((ord(character) - 97 + 9) % 26) + 97))
        return ''.join(result_list)

    @classmethod
    def secret(cls, length: int):
        """
        Generate a random secret of the given length.

        Args:
            length (int): Length of the secret.

        Returns:
            str: The generated secret.
        """
        return ''.join(choice(ASCII_LOWERCASE)
                       for _ in range(length))

    @classmethod
    def decrypt(cls, data: str, key: str):
        """
        Decrypt data using AES encryption.

        Args:
            data (str): The encrypted data.
            key (str): The encryption key.

        Returns:
            dict: The decrypted data as a dictionary.
        """
        decoder = JSONDecoder()
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, cls.AES_IV)
        decoded_data = b64decode(data)
        result, _ = decoder.raw_decode(cipher.decrypt(decoded_data).decode('utf-8'))
        return result

    @classmethod
    def encrypt(cls, data, key):
        """
        Encrypt data using AES encryption.

        Args:
            data (str or dict): The data to be encrypted.
            key (str): The encryption key.

        Returns:
            str: The encrypted data as a string.
        """
        if not isinstance(data, str):
            data = dumps(data, default=lambda x: str(x))

        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, cls.AES_IV)
        length = 16 - (len(data) % 16)
        data += chr(length) * length
        return (
            b64encode(cipher.encrypt(data.encode('utf-8')))
            .decode('utf-8')
        )

    @staticmethod
    def sign(private_key: str, data: str) -> str:
        """
        Sign data using an RSA private key.

        Args:
            private_key (str): The RSA private key.
            data (str): The data to be signed.

        Returns:
            str: The base64-encoded signature.
        """
        key = RSA.import_key(private_key.encode('utf-8'))
        signature = pkcs1_15.new(key).sign(
            SHA256.new(data.encode('utf-8'))
        )
        return b64encode(signature).decode('utf-8')

    @staticmethod
    def create_keys() -> tuple:
        """
        Generate RSA public and private keys.

        Returns:
            tuple: A tuple containing the base64-encoded public key and the private key.
        """
        keys = RSA.generate(1024)
        public_key = Crypto.decode_auth(b64encode(keys.publickey().export_key()).decode('utf-8'))
        private_key = keys.export_key().decode('utf-8')
        return public_key, private_key

    @staticmethod
    def decrypt_RSA_OAEP(private_key: str, data: str):
        """
        Decrypt data using RSA OAEP encryption.

        Args:
            private_key (str): The RSA private key.
            data (str): The encrypted data.

        Returns:
            str: The decrypted data as a string.
        """
        key = RSA.import_key(private_key.encode('utf-8'))
        return PKCS1_OAEP.new(key).decrypt(b64decode(data)).decode('utf-8')