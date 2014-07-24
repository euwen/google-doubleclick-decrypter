# DoubleClick Requests Decrypter
Google DoubleClick Ad Exchange RTB Decrypter in Python

https://travis-ci.org/trein/google-doubleclick-decrypter.svg?branch=master

 - Based on kay-si's [version](https://github.com/kay-si/Google_AdEx_Decrypt)
 - Complete documentation can be found [here](https://developers.google.com/ad-exchange/rtb/)

## Installing
Clone the repository and run `setup.py` as a regular Python library:

```
$ git clone https://github.com/trein/google-doubleclick-decrypter.git
$ cd google-doubleclick-decrypter
$ python setup.py install
```

## Usage
Some examples are available in `samples` directory. Essentially, every time a bid request need to be decrypted, simply create a `Decrypter` object with the correct keys and call the decryption method passing the encrypted text.

```python
from decrypter import DecrypterHyperLocal

decrypter = DecrypterHyperLocal(encryption_encoded_key, integrity_encoded_key)
bid_request = decrypter.deserialize_bid_request(long_ciphertext)
decrypted_request = decrypter.decryption(bid_request.encrypted_hyperlocal_set)
```

## Developing
The Python dependencies can be easily installed by:

```
$ git clone https://github.com/trein/google-doubleclick-decrypter.git
$ cd google-doubleclick-decrypter
$ pip install -r requirements.txt
```

## Generating Protobuf wrappers (optional and for advanced users)
By default, the Protobuf compiler generated Python wrappers are available under `lib` folder. In case you want to update these descriptors, you must install Google Protocol Buffer binaries first.

### Google Protocol Buffer Binaries Dependencies
Usually there are several ways to do that, but here I suggest two:

#### From source code
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

```
$ brew install protobuf
```

### Wrappers generation
There are two Python wrappers that must be generated. These wrappers use `.proto` files, which describe the messages structure.

```
$ cd resources
$ protoc hyperlocal.proto --python_out=../lib
$ protoc realtime-bidding.proto --python_out=../lib
```
