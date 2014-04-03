bruteforce-bitcoin-brainwallet
==============================

A python script that performs a bruteforce dictionary attack on brainwallets. It takes a dictionary input file
 and converts each word into a bitcoin address. It does it lookup of this address (using local Abe (https://github.com/jtobey/bitcoin-abe) or Blockchain.info) to
 see if any bitcoins have ever been received by this address. If an

#Requirements
* Python 2.7, requests, coinkit

#Usage
```
usage: bbb.py [-h] -t TYPE -d DICT_FILE -o OUTPUT_FILE [-s SERVER] [-p PORT]
              [-c CHAIN] [--version]

A script to perform bruteforce dictionary attacks on brainwallets.

optional arguments:
  -h, --help      show this help message and exit
  -t TYPE         Blockchain lookup type (abe|blockchaininfo)
  -d DICT_FILE    Dictionary file (one word per line)
  -o OUTPUT_FILE  Output file (e.g. output.txt)
  -s SERVER       Abe host address (e.g. localhost)
  -p PORT         Abe port (e.g. 2751)
  -c CHAIN        Abe chain string (e.g. Bitcoin)
  --version       show program's version number and exit

```