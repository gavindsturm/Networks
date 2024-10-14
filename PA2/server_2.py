import socket
import sys
import csv

def load_translations(filename):
    translations = {}
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:  
                original, translated = row
                translations[original.strip()] = translated.strip()
            else:
                print(f"Skipping invalid row: {row}") 
    return translations

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
    port = int(sys.argv[1])
    translations = load_translations('pirate.csv')
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))
    print(f"Server listening on port {port}")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        packet_data = eval(data.decode())
        segment = packet_data['message']
        checksum = packet_data['checksum']

        print(f"Received segment: {segment} with checksum: {checksum}")

        ack_packet = Packet(packet_data['sequence_number'], checksum, 1, 0, "")
        server_socket.sendto(str(ack_packet.__dict__).encode(), client_address)
        print(f"Sent ACK for segment: {segment}")

        translated_segment = translations.get(segment, segment)
        translated_packet = Packet(packet_data['sequence_number'], Packet.calculate_checksum(translated_segment), 2, len(translated_segment), translated_segment)
        
        server_socket.sendto(str(translated_packet.__dict__).encode(), client_address)
        print(f"Sent translated segment: {translated_segment}")

if __name__ == "__main__":
    main()
