import math
import random
class CaroBoardGame:
    __table_size = 0
    __table = []
    __human_chess = 0
    __ai_chess = 1
    __scores = {"Win": 10, "Lose": -10, "Draw": 0}

    def __init__(self, size: int) -> None:
        self.__table_size = size
        self.__table = [[-1 for i in range(self.__table_size)] for j in range(self.__table_size)]

    def get_table(self):
        return self.__table

    def put_to_possition(self, x_pos: int, y_pos: int, chess: int):
        if x_pos < self.__table_size and y_pos < self.__table_size and x_pos >= 0 and y_pos >= 0:
            if self.__table[x_pos][y_pos] == -1:
                self.__table[x_pos][y_pos] = chess
                return True
        
        return False

    def display_header(self):
        print("\t", end="")
        for i in range(self.__table_size):
            print(i, end="\t")
        print()

    def display_table(self):
        print("_"*50)
        self.display_header()
        for i in range(self.__table_size):
            print()
            print(i, end='\t')
            for cell in self.__table[i]:
                if cell != -1:
                    print(self.convert_value_chess(cell), end="\t")
                else:
                    print("_", end="\t")
            print()

    def convert_value_chess(self, value):
        if value == 0:
            return "O"
        return "X"

    def check_rows(self, board):
        count_x = 0
        count_o = 0

        for i in range(len(board)):
            count_x = 0
            count_o = 0
            for j in range(len(board[0])):
                if board[i][j] == 1:
                    count_x += 1
                if board[i][j] == 0:
                    count_o += 1
        
            if count_x == len(board) or count_o == len(board):
                return (count_x, count_o)

        return None

    def check_columns(self, board):
        count_x = 0
        count_o = 0
        for i in range(len(board)):
            count_x = 0
            count_o = 0
            for j in range(len(board[0])):
                if board[j][i] == 1:
                    count_x += 1
                if board[j][i] == 0:
                    count_o += 1
        
            if count_x == len(board) or count_o == len(board):
                return (count_x, count_o)
                
        return None
        
    def check_main_cross(self, board):
        count_x = 0
        count_o = 0
        for i in range(len(board)):
            if board[i][i] == 1:
                count_x += 1
            if board[i][i] == 0:
                count_o += 1
        
        if count_x == len(board) or count_o == len(board):
            return (count_x, count_o)

        return None
        
    def check_auxiliary_cross(self, board):
        y_pos = len(board) - 1
        count_x = 0
        count_o = 0
        for x_pos in range(len(board[0])):
            if board[x_pos][y_pos] == 1:
                count_x += 1
            if board[x_pos][y_pos] == 0:
                count_o += 1
            y_pos -= 1

        if count_x == len(board) or count_o == len(board):
            return (count_x, count_o)

        return None

    def winner(self, board):
        board_state = [
            self.check_rows(board), 
            self.check_columns(board), 
            self.check_main_cross(board), 
            self.check_auxiliary_cross(board)
        ]

        winner = 0
        found = False
        
        for state in board_state:
            if state != None:
                row_x, row_o = state
                if row_x > row_o:
                    winner = 1
                    found = True
                    break

        if not found:
            winner = -1

        return winner

    def is_win(self, board):
        return self.winner(board) != -1

    def is_finish(self, board):
        for row in board:
            if -1 in row:
                return False

        return True

    def is_draw(self, board):
        return not self.is_win(board) and self.is_finish(board)

    def check_state(self, board):
        if self.winner(board) == 1:
            return "Win"
        elif self.winner(board) == 0:
            return "Lose"
        elif self.is_draw(board):
            return "Draw"
        else:
            return "n"

    def minimax(self, board, depth, minimize):
        current_state = self.check_state(board)
        if current_state != "n":
            if current_state == "Win":
                return self.__scores[current_state] - depth
            elif current_state == "Lose":
                return self.__scores[current_state] + depth
            else:
                return self.__scores[current_state]
            
        if minimize:
            best_score = -math.inf
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == -1:
                        board[i][j] = self.__ai_chess
                        score = self.minimax(board, depth+1, False)
                        board[i][j] = -1
                        best_score = max(best_score, score)
            
            return best_score

        else:
            best_score = math.inf

            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == -1:
                        board[i][j] = self.__human_chess
                        score = self.minimax(board, depth+1, True)
                        board[i][j] = -1
                        best_score = min(best_score, score)
            
            return best_score

    def is_new_board(self, board):
        count = 0
        for row in board:
            for cell in row:
                if cell == -1:
                    count+=1
        return count == len(board)*len(board[0])
        
    def best_move(self, chess):
        best_score = -math.inf
        board = self.__table
        position = [0, 0]
        if self.is_new_board(board):
            position = [random.randrange(0, len(board)), random.randrange(0, len(board[0]))]
        else:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == -1:
                        board[i][j] = chess
                        score = self.minimax(board, 0, False)
                        board[i][j] = -1
                        if score > best_score:
                            best_score = score
                            position = [i, j]

        self.put_to_possition(position[0], position[1], chess)

    def ai(self, chess):
        self.best_move(chess)

def user_ai(init):
    chess = 1
    while True:
        try:
            if chess == 0:
                print(f"Turn of {chess}: ", end="")
                x_y_pos = input()
                x_y_pos = x_y_pos.strip()
                x_pos, y_pos = tuple(x_y_pos.split(" "))

                if not init.put_to_possition(int(x_pos), int(y_pos), chess):
                    print("Enter again")
                    continue
            else:
                init.ai(chess)

            init.display_table()
            if init.is_win(init.get_table()):
                return chess
            if init.is_draw(init.get_table()):                
                return 100
            
            if chess == 1:
                chess = 0
            else:
                chess = 1
        except ValueError:
            print("Enter again")
        except KeyboardInterrupt:
            break

user_ai(CaroBoardGame(3))