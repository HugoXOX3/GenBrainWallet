import hashlib
import binascii
import base58
import requests
import ecdsa
import bitcoin

KeepRunning = True

def private_key_to_wif(private_key):
    extended_key = b"\x80" + private_key
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
    return base58.b58encode(extended_key + checksum)

def private_key_to_public_key(private_key):
    signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    return bytes.fromhex("04") + verifying_key.to_string()

def WIF(passphrase):
    hashed_passphrase = hashlib.sha256(passphrase.encode()).digest() 
    private_key = hashed_passphrase[:32]
    wif_private_key = private_key_to_wif(private_key).decode()

    return wif_private_key,private_key

def check_balance():
    passphrase = str(input("Enter a Passphrase : "))
    wif_private_key,private_key = WIF(passphrase)
    public_key = private_key_to_public_key(private_key).hex()
    address = bitcoin.pubkey_to_address(public_key)
    try:
        response = requests.get("https://blockchain.info/balance", params={"active": address})
        response.raise_for_status()
        data = response.json()
        final_balance=float(data[address]["final_balance"])
        print(wif_private_key)
        print(address)
        print(final_balance)
    except Exception as e:
        print("Error:Please Check your Network Connection")
        print(e)

while KeepRunning:
    check_balance()