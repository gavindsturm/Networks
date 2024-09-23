import socket
import random

def generate_board():
    board = [[' ' for _ in range(6)] for _ in range(6)]
    ships = [(4, 'A'), (3, 'B'), (2, 'C')]
    ship_locations = []

    def place_ship(length, ship_char):
        placed = False
        while not placed:
            orientation = random.choice(['H', 'V'])
            if orientation == 'H':
                row = random.randint(0, 5)
                col = random.randint(0, 5 - length)
                if all(board[row][col + i] == ' ' for i in range(length)):
                    for i in range(length):
                        board[row][col + i] = ship_char
                    ship_locations.append((row, col, orientation, length))
                    placed = True
            else:
                row = random.randint(0, 5 - length)
                col = random.randint(0, 5)
                if all(board[row + i][col] == ' ' for i in range(length)):
                    for i in range(length):
                        board[row + i][col] = ship_char
                    ship_locations.append((row, col, orientation, length))
                    placed = True

    for length, ship_char in ships:
        place_ship(length, ship_char)
    
    return board, ship_locations

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

def handle_client_connection(client_socket, board, ship_locations):
    hits = 0
    total_ship_cells = sum(length for _, _, _, length in ship_locations)

    while True:
        try:
            guess = client_socket.recv(1024).decode()
            if not guess:
                break
            row, col = map(int, guess.split())
            if 0 <= row < 6 and 0 <= col < 6:
                if board[row][col] != ' ':
                    board[row][col] = 'X'
                    hits += 1
                    client_socket.sendall(b'Hit')
                else:
                    client_socket.sendall(b'Miss')
                
                
                if hits == total_ship_cells:
                    client_socket.sendall(b'Game Over')
                    print("All ships sunk! Game over!")  
                    break
            else:
                client_socket.sendall(b'Invalid')
        except Exception as e:
            print(f"Error handling client: {e}")
            break
    client_socket.close()

def main(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    print(f"Server listening on port {port}...")

    board, ship_locations = generate_board()
    print_board(board)

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            handle_client_connection(client_socket, board, ship_locations)
            break  
    finally:
        server_socket.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    main(port)

