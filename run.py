from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Step 1: Define plaintext message
plaintext = b"O2=19.4;TEMP=24;PRESS=101"

# Step 2: Generate a 256-bit key (32 bytes)
key = get_random_bytes(32)

# Step 3: Create AES cipher (CBC mode)
cipher = AES.new(key, AES.MODE_CBC)

# Step 4: Encrypt the message
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

print("Encrypted Data:", ciphertext)

# Step 5: Decrypt the message
cipher_dec = AES.new(key, AES.MODE_CBC, cipher.iv)
decrypted_text = unpad(cipher_dec.decrypt(ciphertext), AES.block_size)

print("Decrypted Data:", decrypted_text.decode())