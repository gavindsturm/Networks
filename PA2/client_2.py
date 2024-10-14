import socket
import sys
import time

class Packet:
    def __init__(self, sequence_number, checksum, ack_or_nak, length, message):
        self.sequence_number = sequence_number
        self.checksum = checksum
        self.ack_or_nak = ack_or_nak
        self.length = length
        self.message = message

    @staticmethod
    def calculate_checksum(message):
        return sum(ord(char) for char in message)

def main():
    server_ip = 'localhost'
    server_port = int(sys.argv[1])
    sentence = input("Enter a sentence to translate: ")
    segments = sentence.split()
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sequence_number = 1

    translated_sentence = []

    for segment in segments:
        checksum = Packet.calculate_checksum(segment)
        packet = Packet(sequence_number, checksum, 0, len(segment), segment)
        
        while True:
            client_socket.sendto(str(packet.__dict__).encode(), (server_ip, server_port))
            print(f"Sent segment: {segment} with checksum: {checksum}")
            
            try:
                client_socket.settimeout(1)  
                ack_data, _ = client_socket.recvfrom(1024)
                ack_packet = eval(ack_data.decode())
                
                if ack_packet['ack_or_nak'] == 1:  
                    print(f"Received ACK for segment: {segment}")
                    break
            except socket.timeout:
                print("ACK not received, resending segment...")

        translated_data, _ = client_socket.recvfrom(1024)
        translated_packet = eval(translated_data.decode())
        translated_segment = translated_packet['message']
        translated_sentence.append(translated_segment)
        print(f"Received translated segment: {translated_segment}")

    print("Translated sentence:", ' '.join(translated_sentence))

if __name__ == "__main__":
    main()
