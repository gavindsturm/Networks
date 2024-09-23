import socket

def print_board(board):
    print("Current board status:")
    for row in board:
        print(' '.join(row))
    print()

def get_guess():
    while True:
        try:
            row = int(input("Enter row (0-5): "))
            col = int(input("Enter column (0-5): "))
            if 0 <= row < 6 and 0 <= col < 6:
                return row, col
            else:
                print("Invalid input. Row and column must be between 0 and 5.")
        except ValueError:
            print("Invalid input. Please enter numeric values.")

def main(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    board = [[' ' for _ in range(6)] for _ in range(6)]
    guesses = 0
    total_ships = 0
    sunk_ships = 0
    ship_symbols = {'A': 4, 'B': 3, 'C': 2}  

    while True:
        print_board(board)

        row, col = get_guess()
        guess = f"{row} {col}"

        client_socket.sendall(guess.encode())
        response = client_socket.recv(1024).decode()

        if response == 'Hit':
            print("Hit!")
            board[row][col] = 'X'
            guesses += 1
        elif response == 'Miss':
            print("Miss!")
            board[row][col] = 'O'
            guesses += 1
        elif response == 'Invalid':
            print("Invalid guess. Try again.")
        else:
            print("Unexpected response from server.")
            break
        

            print(f"Game over! Total guesses: {guesses}")
            break

    client_socket.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python client.py <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    main(server_ip, server_port)
