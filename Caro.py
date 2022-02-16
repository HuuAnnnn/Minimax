import math
import random

class CaroBoardGame:
    __table_size = 0
    __table = []
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
                    print(" ", end="\t")
            print()

    def convert_value_chess(self, value):
        if value == 0:
            return "O"
        return "X"

    def is_win(self, board):
        return self.check_columns_valid(board) or self.check_row_valid(board) or self.check_main_cross(board) or self.check_auxiliary_cross(board)

    def check_row_valid(self, board):
        for i in range(len(board)):
            count_x = 0
            count_o = 0
            for j in range(len(board)):
                if self.__table[i][j] == 0:
                    count_o += 1
                if self.__table[i][j] == 1:
                        count_x += 1

            if count_x == len(board) or count_o == len(board):
                return True

        return False

    def check_columns_valid(self, board):
        for i in range(len(board)):
            count_x = 0
            count_o = 0
            for j in range(len(board)):
                if self.__table[j][i] == 0:
                    count_o += 1
                if self.__table[j][i] == 1:
                    count_x += 1

            if count_x == len(board) or count_o == len(board):
                return True

        return False

    def check_main_cross(self, board):
        count_x = 0
        count_o = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if i == j:
                    if self.__table[i][j] == 0:
                        count_o += 1
                    if self.__table[i][j] == 1:
                        count_x += 1
                    
        if count_x == len(board) or count_o == len(board):
            return True

        return False

    def check_auxiliary_cross(self, board):
        x = 0
        y = self.__table_size - 1
        count_x = 0
        count_o = 0
        for i in range(len(board)):
            if self.__table[x][y] == 0:
                count_o += 1
            if self.__table[x][y] == 1:
                count_x += 1

            x += 1
            y -= 1
        if count_x == len(board) or count_o == len(board):
            return True
        return False
    
    def is_finish(self, board):
        for i in range(len(board)):
            for j in range(len(board)):
                if self.__table[i][j] == -1:
                    return False

        return True

    def is_draw(self, board):
        return self.is_finish(board) and not self.is_win(board)

    def convert_state_to_value(self, board):
        if self.is_win(board):
            return 1
        elif self.is_draw(board):
            return 0
        else:
            return -1

    def minimax(self, board, depth, maximizing):
        if self.is_finish(board):
            return self.convert_state_to_value(board)

        best_score = 0
        if maximizing:
            maximum = -math.inf            
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == -1:
                        board[i][j] = 1
                        score = self.minimax(board, depth+1, False)
                        board[i][j] = -1
                        best_score = max(maximum, score)

            return best_score
        else:
            minimum = math.inf

            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == -1:
                        board[i][j] = 0
                        score = self.minimax(board, depth+1, True)                  
                        board[i][j] = -1
                        best_score = min(minimum, score)
            
            return best_score

    def is_new_board(self, board):
        for row in board:
            for cell in row:
                if cell != -1:
                    return False
        return True

    def best_move(self, chess):
        best_score = -math.inf
        board = self.__table.copy()
        position = []
        if self.is_new_board(board):
            position = [random.randrange(self.__table_size), random.randrange(self.__table_size)]
        else:
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] == -1:
                        board[i][j] = 1
                        score = self.minimax(board, 0, True)
                        board[i][j] = -1
                        if best_score < score:
                            best_score = score
                            position = [i, j]

        self.put_to_possition(position[0], position[1], chess)

def user_ai(init):
    chess = 0
    while True:
        try:
            if chess == 1:
                print(f"Turn of {chess}: ", end="")
                x_y_pos = input()
                x_y_pos = x_y_pos.strip()
                x_pos, y_pos = tuple(x_y_pos.split(" "))

                if not init.put_to_possition(int(x_pos), int(y_pos), chess):
                    print("Enter again")
            else:
                init.best_move(chess)

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

def ai_ai(init):
    chess = 0
    while True:
        try:
            init.best_move(chess)

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
