import socket
import random
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


SHARED_SECRET = "csci466"  
KEY = "0123456789ABCDEF"  
BLOCK_SIZE = 32            
SERVER_HOST = '127.0.0.1'  
SERVER_PORT = 65432        

def encrypt_message(key, message):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(message.encode(), BLOCK_SIZE))
    return ciphertext

def compute_mac(message, shared_secret):
    concatenated = message + shared_secret
    return sha256(concatenated.encode()).hexdigest()

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print("Attempting to connect to the server...")
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print("Connected to the server.")

            while True:
                message = input("Enter a message to send (or 'exit' to quit): ").strip()
                if message.lower() == 'exit':
                    print("Exiting the client...")
                    break

                encrypted_message = encrypt_message(KEY, message)
                print(f"Encrypted message: {encrypted_message}")

                mac = compute_mac(message, SHARED_SECRET)

                if random.random() <= 0.5:
                    print("Corrupting the message...")
                    message = "corrupted"
                    mac = compute_mac(message, SHARED_SECRET)

                print("Sending encrypted message and MAC to the server...")
                client_socket.sendall(encrypted_message)
                client_socket.sendall(mac.encode())

                print(f"Sent message: {message}")
                print(f"Sent MAC: {mac}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
