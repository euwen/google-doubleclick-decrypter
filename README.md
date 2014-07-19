# DoubleClick Requests Decrypter
Google Decrypter for DoubleClick Ad Exchange Requests

 - Based on kay-si's [version](https://github.com/kay-si/Google_AdEx_Decrypt)
 - Complete documentation can be found [here](https://developers.google.com/ad-exchange/rtb/)

## Dependencies

### Google Protocol Buffer Binaries Dependencies

#### From source
Download from [Google Code](https://code.google.com/p/protobuf/) and issue the commands:

```
$ mkdir ~/protobuf && cd ~/protobuf
$ curl -o protobuf-2.5.0.tar.bz https://protobuf.googlecode.com/files/protobuf-2.5.0.tar.bz
$ tar -xzf protobuf-2.5.0.tar.gz
$ cd protobuf-2.5.0
$ ./configure
$ make
$ sudo make install
```

#### With Homebrew
Simply issue the command:

    $ brew install protobuf

### Python Dependencies
The Python dependencies can be easily installed by:

    $ pip install -r requirements.txt


## Usage
Some examples are available in `samples` directory. Essentially, every time a bid request need to be decrypted, simply create a `Decrypter` object with the correct keys and call the decryption method passing the encrypted text.

```python
decrypter = DecrypterHyperLocal(encryption_encoded_key, integrity_encoded_key)
bid_request = decrypter.deserialize_bid_request(long_ciphertext)
decrypted_request = decrypter.decryption(bid_request.encrypted_hyperlocal_set)
```