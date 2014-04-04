from coinkit import BitcoinKeypair
import logging


class BrainWallet:
    def __init__(self, passphrase):
        self.passphrase = passphrase
        self.address = None
        self.public_key = None
        self.private_key = None
        try:
            keypair = BitcoinKeypair.from_passphrase(self.passphrase)
            self.address = keypair.address()
            self.public_key = keypair.public_key()
            self.private_key = keypair.private_key()
        except Exception as e:
            logging.warning("Failed to generate keypair for passphrase '{}'. Error: {}".format(passphrase, e.args))
