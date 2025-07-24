import sys
import segno
from tqdm import tqdm
import time

import secrets
import base64
import hmac
import hashlib
import struct


def generate_shared_secret():
    return secrets.token_bytes(10)


def gen_qr(user_id):
    # Example URI: otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example
    code1 = "otpauth://totp/Google%20Authenticator:"
    code2 = "?secret="
    code3 = "&issuer=Google%20Authenticator"

    # generate secret key
    secret = base64.b32encode(generate_shared_secret()).decode('utf-8')
    
    uri = code1+user_id+code2+secret+code3
    print(" >> URI generated: ", uri)

    # store secret
    file = open("secret.txt", "w") 
    file.write(secret)
    file.close()

    # generate qr code based on uri
    qrcode = segno.make(uri, micro=False)
    qrcode.save('qr_code.png')

    return


# def generate_otp(secret, digits=6, time_step=30):
#     # decode the base32-encoded secret to bytes'
#     key = base64.b32decode(secret, casefold=True)
#     # convert current time step to a byte array in big-endian format
#     counter_bytes = struct.pack(">Q", int(time.time() / time_step))
#     # generate an HMAC-SHA1 digest from the counter and the secret key
#     hmac_digest = hmac.new(key, counter_bytes, hashlib.sha1).digest()
    
#     # determine the offset
#     offset = hmac_digest[-1] & 0x0F
#     # extracting a 4-byte segment from the HMAC result
#     seg1 = struct.unpack(">I", hmac_digest[offset:offset+4])[0]
#     # removing the most significant bit:
#     seg2 = seg1 & 0x7FFFFFFF
    
#     # generate the OTP
#     otp = seg2 % (10 ** digits)
#     return otp


def generate_otp(secret_base32, digits=6, time_step=30):
    # Step 1: Decode the base32-encoded secret string into raw bytes
    key = base64.b32decode(secret_base32, casefold=True)

    # Step 2: Get the current time step
    current_time = int(time.time())  # Current Unix time in seconds
    counter = current_time // time_step  # Which 30-second window we're in

    # Step 3: Convert the counter to an 8-byte big-endian byte array
    counter_bytes = struct.pack(">Q", counter)

    # Step 4: Create an HMAC-SHA1 hash using the secret key and the counter
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    # Step 5: Dynamic offset is the last nibble (4 bits) of the HMAC
    # This chooses where to start slicing the hash
    offset = hmac_hash[-1] & 0x0F  # Value between 0 and 15

    # Step 6: Take 4 bytes starting at the offset
    selected_bytes = hmac_hash[offset:offset + 4]

    # Step 7: Convert those 4 bytes to a big-endian integer
    code_int = struct.unpack(">I", selected_bytes)[0]

    # Step 8: Remove the sign bit (make sure the number is positive)
    code_int = code_int & 0x7FFFFFFF

    # Step 9: Reduce it to the number of digits we want (e.g., 6)
    otp = code_int % (10 ** digits)

    return otp



def get_otp(t=30):
    file = open("secret.txt", "r")
    secret = file.readline()
    file.close()
    while True:
        otp = generate_otp(secret)
        print(" > Generated OTP:", otp, "valid for", int(t-(time.time()%t))+1, "seconds")
        for i in tqdm (range(int(t-(time.time()%t))+1), 
               desc="Loading…", 
               ascii=False, ncols=75):
            time.sleep(1)



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(" >> Invalid flag: can either be \"--generate-qr [user_id]\" or \"--get-otp\"")
    elif sys.argv[1] == "--generate-qr" and len(sys.argv) == 3:
        gen_qr(sys.argv[2])
    elif sys.argv[1] == "--get-otp" and len(sys.argv) == 2:
        get_otp()
    else:
        print(" >> Invalid flag: can either be \"--generate-qr [user_id]\" or \"--get-otp\"")