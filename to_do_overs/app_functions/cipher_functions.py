#!/usr/bin/env python
"""
Cipher functions for the Habitica To Do Over tool.
"""

__author__ = "Katie Patterson kirska.com"
__license__ = "MIT"

import argparse
from cryptography.fernet import Fernet
from local_defines import CIPHER_FILE


def generate_cipher_key():
    """Generates a cipher key.

    Generates a cipher key to be used for storing sensitive data in the database.
    This will make all existing data GARBAGE so use with caution.
    """
    key = Fernet.generate_key()
    with open(CIPHER_FILE, 'wb') as cipher_file:
        cipher_file.write(key)


def encrypt_text(text):
    """Encrypt some text using the cipher key.

    Read the cipher key from file and use it to encrypt some text.

    Args:
        text: the text to be encrypted.

    Returns:
        The encrypted text.
    """
    with open(CIPHER_FILE, 'rb') as cipher_file:
        key = cipher_file.read()
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(text)
        return cipher_text


def decrypt_text(cipher_text, cipher_file=CIPHER_FILE):
    """Decrypt some text back into the plain text.

    Read the cipher key from file and use it to decrypt some text.

    Args:
        cipher_text: the encrypted text we want to decrypt.

    Returns:
        The decrypted text.
    """
    with open(CIPHER_FILE, 'rb') as cipher_file:
        key = cipher_file.read()
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(cipher_text)
        return plain_text


def test_cipher(test_text):
    """Test the cipher functions.

    Encrypt and then decrypt some text using the cipher stored in the cipher file.

    Args:
        test_text: some plain text we want to test encrypting and decrypting.
    """
    cipher_text = encrypt_text(test_text)
    print cipher_text
    plain_text = decrypt_text(cipher_text)
    print plain_text

"""
parser = argparse.ArgumentParser(description='Generate a cipher.')
parser.add_argument('--generate', action='store_true',
                    help='generate a new cipher and store in a file USE WITH CAUTION')
parser.add_argument('--test', help='test your existing cipher')

args = parser.parse_args()

if args.generate:
    generate_cipher_key()
elif args.test:
    test_cipher(args.test)
"""