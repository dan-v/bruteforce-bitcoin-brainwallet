from coinkit import BitcoinKeypair
import logging


class Wallet:
    def __init__(self, passphrase, is_private_key = False):
        self.passphrase = passphrase
        self.address = None
        self.public_key = None
        self.private_key = None
        try:
            if is_private_key:
                keypair = BitcoinKeypair.from_private_key(self.passphrase.encode('ascii'))
            else:
                keypair = BitcoinKeypair.from_passphrase(self.passphrase)
            self.address = keypair.address()
            self.public_key = keypair.public_key()
            self.private_key = keypair.private_key()
        except Exception as e:
            logging.warning(u"Failed to generate keypair for passphrase '{}'. Error: {}".format(passphrase, e.args))
            raise