import socket
import sys
import random
import time
import threading

class Node:
    def __init__(self, send_port, receive_port, buffer_size, is_head, node_number):
        self.send_port = send_port
        self.receive_port = receive_port
        self.buffer_size = buffer_size
        self.is_head = is_head
        self.node_number = node_number
        self.buffer = buffer_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', self.receive_port))

        print(f"Node {self.node_number} initialized. Send port: {self.send_port}, Receive port: {self.receive_port}, Buffer size: {self.buffer_size}.")

        threading.Thread(target=self.receive_token, daemon=True).start()

        if self.is_head:
            print(f"Node {self.node_number} is the head. Sending initial token...")
            self.send_token()

    def send_token(self):
        message = f"TOKEN|Node {self.node_number}|Buffer {self.buffer}".encode()
        print(f"Node {self.node_number} preparing to send: {message.decode()}")
        try:
            self.sock.sendto(message, ('localhost', self.send_port))
            print(f"Node {self.node_number} sent: {message.decode()}")
            time.sleep(1) 
        except Exception as e:
            print(f"Node {self.node_number} failed to send: {e}")

    def receive_token(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                print(f"Node {self.node_number} received data from {addr}: {data.decode()}")
                if data.startswith(b'TOKEN'):
                    self.handle_token(data.decode())
            except Exception as e:
                print(f"Node {self.node_number} encountered an unexpected error: {e}")
                time.sleep(1) 

    def handle_token(self, message):
        print(f"Node {self.node_number} processing received token: {message}")
        token_info = message.split('|')
        
        if len(token_info) == 3:
            received_node = token_info[1]
            received_buffer = token_info[2]
            print(f"Node {self.node_number} processing received token from {received_node} with {received_buffer}.")
        
        if self.buffer > 0:
            print(f"Node {self.node_number} has packets to send. Current buffer size: {self.buffer}. Sending packet...")
            self.buffer -= 1 
            self.send_token()
            self.maybe_add_to_buffer()
        else:
            print(f"Node {self.node_number} has nothing to send. Passing token to next node...")
            self.send_token()
            self.maybe_add_to_buffer()

    def maybe_add_to_buffer(self):
        if random.random() < 0.25:  
            self.buffer += 1
            print(f"Node {self.node_number} added to buffer. Current buffer size: {self.buffer}.")
            time.sleep(1)  

def main():
    if len(sys.argv) != 6:
        print("Usage: python node.py (send_port) (receive_port) (#_of_packets_in_buffer) (is_head) (node_#)")
        sys.exit(1)

    send_port = int(sys.argv[1])
    receive_port = int(sys.argv[2])
    buffer_size = int(sys.argv[3])
    is_head = bool(int(sys.argv[4]))
    node_number = int(sys.argv[5])

    node = Node(send_port, receive_port, buffer_size, is_head, node_number)

   
    while True:
        time.sleep(1)  

if __name__ == "__main__":
    main()
