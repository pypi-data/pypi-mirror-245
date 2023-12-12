

import os
from pwrpy.pwrwallet import PWRWallet

wallet = PWRWallet()


def test_get_address():
    assert wallet.get_address().startswith("0x") == True


def test_get_private_key():
    assert wallet.get_private_key() != None


def test_get_public_key():
    assert wallet.get_public_key() != None


def test_get_nonce():
    assert wallet.get_balance() != None
