import sys
import segno
from tqdm import tqdm
import time

import secrets
import base64
import hmac
import hashlib
import struct


# ========= function for generating a secret ========
def generate_shared_secret():
    return secrets.token_bytes(10)


# ========= function for generating the QR code ========
def gen_qr(user_id):
    # Example URI: otpauth://totp/Authy:alice@example.com?secret=JBSWY3DPEHPK3PXP&issuer=Authy
    code1 = "otpauth://totp/Authy:"
    code2 = "?secret="
    code3 = "&issuer=Authy"

    # generate a new shared secret and base32-encode it
    secret = base64.b32encode(generate_shared_secret()).decode('utf-8')

    # combine parts to form the URI
    uri = f"{code1}{user_id}{code2}{secret}{code3}"
    print(" >> URI generated:", uri)

    # store secret into a file named "secret.txt"
    with open("secret.txt", "w") as f:
        f.write(secret)
    print(" >> Secret saved to secret.txt")

    # generate QR code based on the URI using segno
    qrcode = segno.make(uri, micro=False)
    qrcode.save('qr_code.png')
    print(" >> QR code saved as qr_code.png")


# ========= function for generating the One-Time Password ========
def generate_otp(secret_base32, digits=6, time_step=30):
    # decode the base32-encoded secret string into raw bytes
    key = base64.b32decode(secret_base32, casefold=True)

    # get the current time step
    current_time = time.time()
    counter = int(current_time / time_step)

    # convert the counter to an 8-byte big-endian byte array
    counter_bytes = struct.pack(">Q", counter)

    # create an HMAC-SHA1 hash using the secret key and the counter
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    # the dynamic offset is the last nibble (4 bits) of the HMAC
    offset = hmac_hash[-1] & 0x0F  # value between 0 and 15

    # take 4 bytes of hmac hash starting at the offset
    selected_bytes = hmac_hash[offset:offset + 4]

    # convert those 4 bytes to a big-endian integer
    code_int = struct.unpack(">I", selected_bytes)[0]

    # remove the sign bit (0x7FFFFFFF)
    code_int &= 0x7FFFFFFF

    # get only the requested number of digits
    otp = str(code_int % (10 ** digits)).zfill(digits)

    return otp


# ========= function for displaying OTP every 30 sec ========
def get_otp(t=30):
    # open and read file containing secret
    with open("secret.txt", "r") as f:
        secret = f.readline().strip()

    while True:
        otp = generate_otp(secret)
        valid_secs = int(t - (time.time() % t))
        print(f" > Generated OTP: {otp} valid for {valid_secs + 1} seconds")
        # wait until the next time step, showing progress
        for _ in tqdm(range(valid_secs + 1), desc="Loading…", ascii=False, ncols=75):
            time.sleep(1)


# ========= main function for command handling ========
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(" >> Invalid flag: use '--generate-qr [user_id]' or '--get-otp'")
    elif sys.argv[1] == "--generate-qr" and len(sys.argv) == 3:
        gen_qr(sys.argv[2])
    elif sys.argv[1] == "--get-otp" and len(sys.argv) == 2:
        get_otp()
    else:
        print(" >> Invalid flag: use '--generate-qr [user_id]' or '--get-otp'")
