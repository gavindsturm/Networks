import socket
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

SHARED_SECRET = "csci466"
KEY = "0123456789ABCDEF" 
BLOCK_SIZE = 32  
SERVER_HOST = '127.0.0.1'  
SERVER_PORT = 65432        

def decrypt_message(key, ciphertext):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
    return plaintext.decode()

def compute_mac(message, shared_secret):
    concatenated = message + shared_secret
    return sha256(concatenated.encode()).hexdigest()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(1)
        print("Server is listening...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")

            while True:
                encrypted_message = conn.recv(1024)
                received_mac = conn.recv(1024).decode()

                if not encrypted_message or not received_mac:
                    break

                try:
                    message = decrypt_message(KEY, encrypted_message)
                    print(f"Decrypted message: {message}")

                    computed_mac = compute_mac(message, SHARED_SECRET)
                    if computed_mac == received_mac:
                        print("Packet Accepted: MACs match.")
                    else:
                        print("Packet Rejected: MACs do not match.")
                except Exception as e:
                    print(f"Error: {e}")
                    print("Packet Rejected.")

if __name__ == "__main__":
    main()
