import copy
import random

BOARD_SIZE = 5
WIN_LENGTH = 4
SIMULATIONS = 200  # liczba symulacji dla każdego ruchu

# ===============================
#          KÓŁKO-KRZYŻYK
# ===============================
def create_board():
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def print_board(board):
    symbols = {1:"X", -1:"O", 0:"."}
    for row in board:
        print(" ".join(symbols[x] for x in row))
    print()

def check_winner(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                continue
            player = board[i][j]
            # poziomo
            if j + WIN_LENGTH <= BOARD_SIZE and all(board[i][j+k] == player for k in range(WIN_LENGTH)):
                return player
            # pionowo
            if i + WIN_LENGTH <= BOARD_SIZE and all(board[i+k][j] == player for k in range(WIN_LENGTH)):
                return player
            # diagonal \
            if i + WIN_LENGTH <= BOARD_SIZE and j + WIN_LENGTH <= BOARD_SIZE and all(board[i+k][j+k] == player for k in range(WIN_LENGTH)):
                return player
            # diagonal /
            if i + WIN_LENGTH <= BOARD_SIZE and j - WIN_LENGTH + 1 >= 0 and all(board[i+k][j-k] == player for k in range(WIN_LENGTH)):
                return player
    # remis
    if all(board[i][j] != 0 for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
        return 0
    return None

# ===============================
#         LOSOWA SYMULACJA
# ===============================
def random_playout(board, player):
    b = copy.deepcopy(board)
    current = player
    while True:
        winner = check_winner(b)
        if winner is not None:
            return winner
        moves = [(i,j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if b[i][j]==0]
        move = random.choice(moves)
        b[move[0]][move[1]] = current
        current *= -1

# ===============================
#         MONTE CARLO AI
# ===============================
def monte_carlo_move(board, player, simulations=SIMULATIONS):
    moves = [(i,j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j]==0]
    if not moves:
        return None
    scores = {move:0 for move in moves}
    for move in moves:
        for _ in range(simulations):
            b = copy.deepcopy(board)
            b[move[0]][move[1]] = player
            winner = random_playout(b, -player)
            if winner == player:
                scores[move] += 1
            elif winner == 0:
                scores[move] += 0.5  # remis
            # przegrana = 0
    best_move = max(scores, key=lambda k: scores[k])
    return best_move

# ===============================
#              MAIN
# ===============================
if __name__=="__main__":
    board = create_board()
    current_player = 1  # 1 = X, -1 = O

    while True:
        print_board(board)
        winner = check_winner(board)
        if winner is not None:
            if winner == 1:
                print("X wygrywa!")
            elif winner == -1:
                print("O wygrywa!")
            else:
                print("Remis!")
            break

        if current_player == 1:
            print("Ruch AI (X)...")
            move = monte_carlo_move(board, 1)
            if move:
                board[move[0]][move[1]] = 1
        else:
            print("Ruch przeciwnika (O)...")
            moves = [(i,j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j]==0]
            move = random.choice(moves)  # prosty przeciwnik losowy
            board[move[0]][move[1]] = -1

        current_player *= -1
