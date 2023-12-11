from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import base64


class RSACrypt:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        """
        Generates a pair of RSA keys (private and public key).

        Returns:
            None
        """
        key = RSA.generate(2048)
        self.private_key = key
        self.public_key = key.publickey()

    def export_keys(self):
        """
        Export the private and public keys to files named 'private.pem' and 'public.pem' respectively.

        Raises:
            Exception: If either the private key or the public key is None.

        Returns:
            None
        """
        if self.private_key is None or self.public_key is None:
            raise Exception("no keys to export")

        with open("private.pem", "wb") as f:
            f.write(self.private_key.export_key())

        with open("public.pem", "wb") as f:
            f.write(self.public_key.export_key())

    def load_private_key(self, path):
        """
        Loads the private key from the "private.pem" file and assigns it to the `private_key` attribute.

        Returns:
            None
        """
        with open(path, "rb") as f:
            self.private_key = RSA.import_key(f.read())

    def load_public_key(self, path):
        """
        Loads the public key from the 'public.pem' file.

        Returns:
            None
        """
        with open(path, "rb") as f:
            self.public_key = RSA.import_key(f.read())

    def encrypt(self, message):
        """
        Encrypts the given message using RSA and AES encryption.

        Args:
            message (str or bytes): The message to be encrypted.

        Returns:
            str: The encrypted message encoded in base64.

        Raises:
            Exception: If the public key is not loaded.
        """
        if self.public_key is None:
            raise Exception("load public key first")

        session_key = get_random_bytes(16)

        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        encrypted_session_key = cipher_rsa.encrypt(session_key)

        if type(message) == str:
            message = message.encode("utf-8")

        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        cipher_text, tag = cipher_aes.encrypt_and_digest(message)
        result = encrypted_session_key + cipher_aes.nonce + tag + cipher_text

        return base64.b64encode(result).decode("utf-8")

    def decrypt(self, cipher_text):
        """
        Decrypts the given cipher text using the private key.

        Args:
            cipher_text (str): The cipher text (base64) to be decrypted.

        Returns:
            str: The decrypted data.

        Raises:
            Exception: If the private key is not loaded.
        """
        if self.private_key is None:
            raise Exception("load private key first")

        cipher_text = base64.b64decode(cipher_text)

        encrypted_session_key = cipher_text[: self.private_key.size_in_bytes()]
        nonce = cipher_text[
            self.private_key.size_in_bytes() : self.private_key.size_in_bytes() + 16
        ]
        tag = cipher_text[
            self.private_key.size_in_bytes()
            + 16 : self.private_key.size_in_bytes()
            + 32
        ]
        cipher_text = cipher_text[self.private_key.size_in_bytes() + 32 :]

        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        session_key = cipher_rsa.decrypt(encrypted_session_key)

        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(cipher_text, tag)

        return data.decode("utf-8")
