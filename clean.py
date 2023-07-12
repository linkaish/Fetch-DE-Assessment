import pandas as pd
from datetime import date
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt(message, key):
    # Generate a random 16-byte IV (Initialization Vector)
    if type(message) == float:
        return message
    iv = get_random_bytes(16)

    # Create AES cipher object in CBC mode with the provided key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the IP address to match the block size
    padded_ip = pad(message.encode(), 16)

    # Encrypt the padded IP address
    ciphertext = cipher.encrypt(padded_ip)

    # Return the IV and ciphertext as bytes
    return iv + ciphertext


def decrypt(ciphertext, key):
    # Extract the IV and ciphertext from the input
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    # Create AES cipher object in CBC mode with the provided key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext and remove the padding
    decrypted_ip = unpad(cipher.decrypt(ciphertext), 16)

    # Convert the decrypted bytes to IP address string
    message = decrypted_ip.decode()

    # Return the decrypted IP address
    return message


df = pd.read_csv("user_logins.csv")
encryption_key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'

# Encrypting
# df["ip"] = df["ip"].apply(lambda x: encrypt(x, encryption_key))
# df["device_id"] = df["device_id"].apply(lambda x: encrypt(x, encryption_key))
df["current_date"] = date.today()

# Write to csv
df = df.rename(columns={"ip": "masked_ip", "device_id": "masked_device_id"})
df.to_csv("masked_user_logins.csv", index=False)