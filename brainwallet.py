from coinkit import BitcoinKeypair


class BrainWallet:
    def __init__(self, passphrase):
        self.passphrase = passphrase
        keypair = BitcoinKeypair.from_passphrase(self.passphrase)
        self.address = keypair.address()
        self.public_key = keypair.public_key()
        self.private_key = keypair.private_key()