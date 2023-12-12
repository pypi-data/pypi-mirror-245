

from pwrpy.pwrwallet import PWRWallet


wallet = PWRWallet()


def test_answer():

    assert wallet.get_address() != None
