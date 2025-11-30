import random
import math

# ============================================================
#                 TIC TAC TOE MINIMAX
# ============================================================

def check_winner(board):
    for row in board:
        if row.count(1) == 3: return 1
        if row.count(-1) == 3: return -1
    for i in range(3):
        col = [board[0][i], board[1][i], board[2][i]]
        if col.count(1) == 3: return 1
        if col.count(-1) == 3: return -1
    diag1 = [board[0][0], board[1][1], board[2][2]]
    diag2 = [board[0][2], board[1][1], board[2][0]]
    for d in [diag1, diag2]:
        if d.count(1) == 3: return 1
        if d.count(-1) == 3: return -1
    if all(x != 0 for row in board for x in row):
        return 0
    return None

def minimax(board, player):
    winner = check_winner(board)
    if winner is not None:
        if winner == 1: return 1, None
        elif winner == -1: return -1, None
        else: return 0, None

    best_score = -999 if player == 1 else 999
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = player
                score, _ = minimax(board, -player)
                board[i][j] = 0
                if player == 1 and score > best_score:
                    best_score = score
                    best_move = (i, j)
                if player == -1 and score < best_score:
                    best_score = score
                    best_move = (i, j)
    return best_score, best_move

# ============================================================
#             GENEROWANIE DANYCH TRENINGOWYCH
# ============================================================

def generate_training_data(max_samples=5000):
    X, y = [], []
    visited = set()
    def board_to_tuple(board):
        return tuple([x for row in board for x in row])
    def generate(board, player):
        winner = check_winner(board)
        if winner is not None: return
        key = board_to_tuple(board)
        if key in visited: return
        visited.add(key)
        _, move = minimax(board, player)
        if move is not None:
            X.append([x for row in board for x in row])
            y_vec = [0]*9
            y_vec[move[0]*3 + move[1]] = 1
            y.append(y_vec)
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = player
                    generate(board, -player)
                    board[i][j] = 0
    generate([[0]*3 for _ in range(3)], 1)
    return X[:max_samples], y[:max_samples]

# ============================================================
#                  SIEĆ NEURONOWA W CZYSTYM PYTHON
# ============================================================

def relu(x):
    return max(0, x)

def softmax(x):
    max_x = max(x)
    exps = [math.exp(v - max_x) for v in x]
    s = sum(exps)
    return [v / s for v in exps]

class NeuralNetSL:
    def __init__(self, input_size=9, hidden_size=27, output_size=9):
        # inicjalizacja wag losowo
        self.W1 = [[random.uniform(-0.1,0.1) for _ in range(input_size)] for _ in range(hidden_size)]
        self.b1 = [0]*hidden_size
        self.W2 = [[random.uniform(-0.1,0.1) for _ in range(hidden_size)] for _ in range(output_size)]
        self.b2 = [0]*output_size

    def forward(self, x):
        # warstwa ukryta
        self.z1 = [relu(sum(w*v for w,v in zip(row,x)) + b) for row,b in zip(self.W1,self.b1)]
        # warstwa wyjściowa
        z2 = [sum(w*v for w,v in zip(row,self.z1)) + b for row,b in zip(self.W2,self.b2)]
        self.out = softmax(z2)
        return self.out

    def train(self, X, Y, epochs=200, lr=0.01):
        for epoch in range(epochs):
            loss = 0
            for x, y in zip(X,Y):
                # forward
                out = self.forward(x)
                loss += -sum(y_i*math.log(o_i+1e-9) for y_i,o_i in zip(y,out))
                # gradient dla wyjścia
                dz2 = [o_i - y_i for o_i,y_i in zip(out,y)]
                # gradient W2
                dW2 = [[dz2_i * self.z1[j] for j in range(len(self.z1))] for dz2_i in dz2]
                db2 = dz2[:]
                # gradient warstwy ukrytej
                dz1 = []
                for j in range(len(self.z1)):
                    s = sum(self.W2[i][j]*dz2[i] for i in range(len(dz2)))
                    dz1.append(s if self.z1[j]>0 else 0)
                dW1 = [[dz1[j]*x[i] for i in range(len(x))] for j in range(len(dz1))]
                db1 = dz1[:]
                # update wag
                for i in range(len(self.W1)):
                    for j in range(len(self.W1[0])):
                        self.W1[i][j] -= lr*dW1[i][j]
                    self.b1[i] -= lr*db1[i]
                for i in range(len(self.W2)):
                    for j in range(len(self.W2[0])):
                        self.W2[i][j] -= lr*dW2[i][j]
                    self.b2[i] -= lr*db2[i]
            if epoch%20==0:
                print(f"Epoch {epoch}, loss {loss:.3f}")

    def predict(self, board):
        x = [b for row in board for b in row]
        probs = self.forward(x)
        legal = [i for i,val in enumerate(x) if val==0]
        best = max(legal, key=lambda i: probs[i])
        return [best//3, best%3]

# ============================================================
#                 WYŚWIETLANIE PLANSZY
# ============================================================

def print_board(board):
    symbols = {1:"X",-1:"O",0:"."}
    for row in board:
        print(" ".join(symbols[x] for x in row))
    print()

# ============================================================
#                           MAIN
# ============================================================

if __name__=="__main__":
    print("Generowanie danych treningowych...")
    X,Y = generate_training_data(max_samples=5000)
    print(f"Liczba próbek: {len(X)}")

    print("Trening sieci neuronowej...")
    nn = NeuralNetSL()
    nn.train(X,Y,epochs=40,lr=0.01)

    # testowa plansza 1
    test_board = [
        [1,1,0],
        [-1,-1,0],
        [0,0,0]
    ]

    print("\nPlansza przed ruchem AI:")
    print_board(test_board)
    move = nn.predict(test_board)
    print("AI wybiera ruch:", move)
    test_board[move[0]][move[1]] = 1
    print("Plansza po ruchu AI:")
    print_board(test_board)

    # testowa plansza
    test_board = [
        [-1,1,0],
        [-1,-1,0],
        [1,0,0]
    ]

    print("\nPlansza przed ruchem AI:")
    print_board(test_board)
    move = nn.predict(test_board)
    print("AI wybiera ruch:", move)
    test_board[move[0]][move[1]] = 1
    print("Plansza po ruchu AI:")
    print_board(test_board)