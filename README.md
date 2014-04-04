bruteforce-bitcoin-brainwallet
==============================

A python script that performs a bruteforce dictionary attack on brainwallets. It takes a dictionary input file
 and converts each word into a bitcoin address. A lookup of this address is done either using a local [Abe](https://github.com/jtobey/bitcoin-abe)
 instance or blockchain.info) to see if any bitcoins have ever been received by this address. If so, it will do one more check
 to see the current balance for the bitcoin address.

#Requirements
* Python 2.7, requests, coinkit
<pre>
pip install -r requirements.txt
</pre>

#Usage
```
usage: bbb.py [-h] -t TYPE -d DICT_FILE -o OUTPUT_FILE [-s SERVER] [-p PORT]
              [-c CHAIN] [--version]

A script to perform bruteforce dictionary attacks on brainwallets.

optional arguments:
  -h, --help      show this help message and exit
  -t TYPE         Blockchain lookup type (abe|blockchaininfo)
  -d DICT_FILE    Dictionary input file (one word per line)
  -o OUTPUT_FILE  Output file (outputs <dictionary word>:<wallet address>:<private key>:<current balance>)
  -s SERVER       Abe host address (e.g. localhost)
  -p PORT         Abe port (e.g. 2751)
  -c CHAIN        Abe chain string (e.g. Bitcoin)
  --version       show program's version number and exit
```

#Abe Example
```
python bbb.py -t abe -d dictionary.txt -o found.txt -s 127.0.0.1 -p 2751 -c Bitcoin
```

#Blockchain.info Example
```
python bbb.py -t blockchaininfo -d dictionary.txt -o found.txt
```