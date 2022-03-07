import math
import random

class Caro:
    __table_size = 0
    __table = []
    __human_chess = 0
    __ai_chess = 1
    __scores = {"Win": 10, "Lose": -10, "Draw": 0}
    __chess_value = {0: 'O', 1: 'X'}

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

    def __display_header(self):
        print("\t", end="")
        for i in range(self.__table_size):
            print(i, end="\t")
        print()

    def display_table(self):
        print("_"*(self.__table_size+1+7*(self.__table_size+1)))
        self.__display_header()
        for i in range(self.__table_size):
            print()
            print(i, end='\t')
            for cell in self.__table[i]:
                if cell != -1:
                    print(self.__chess_value[cell], end="\t")
                else:
                    print("_", end="\t")
            print()

    def __check_rows(self, board):
        for i in range(len(board)):
            count_x = board[i].count(1)
            count_o = board[i].count(0)

            if count_x == len(board) or count_o == len(board):
                return (count_x, count_o)

        return None

    def __check_columns(self, board):
        for i in range(len(board)):
            col = [board[j][i] for j in range(len(board[0]))]
            count_x = col.count(1)
            count_o = col.count(0)
                    
            if count_x == len(board) or count_o == len(board):
                return (count_x, count_o)
                
        return None
        
    def __check_main_cross(self, board):
        main_cross = [board[i][i] for i in range(len(board))]
        count_x = main_cross.count(1)
        count_o = main_cross.count(0)
        
        if count_x == len(board) or count_o == len(board):
            return (count_x, count_o)

        return None
        
    def __check_auxiliary_cross(self, board):
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

    def __winner(self, board):
        states = [
            self.__check_rows(board),
            self.__check_columns(board),
            self.__check_main_cross(board),
            self.__check_auxiliary_cross(board)
        ]

        win = 0
        is_found = False

        for state in states:
            if state:
                row_x, row_o = state
                if row_x > row_o:
                    win = 1
                    
                is_found = True
                break
        
        if not is_found:
            win = -1

        return win

    def is_win(self, board):
        return self.__winner(board) != -1

    def __is_finish(self, board):
        for row in board:
            if -1 in row:
                return False

        return True

    def is_draw(self, board):
        return not self.is_win(board) and self.__is_finish(board)

    def __check_state(self, board):
        if self.__winner(board) == 1:
            return "Win"
        elif self.__winner(board) == 0:
            return "Lose"
        elif self.is_draw(board):
            return "Draw"
        else:
            return None
    
    def __evaluation(self, state, depth):
        if state:
            if state == "Win":
                return self.__scores[state] - depth
            elif state == "Lose":
                return self.__scores[state] + depth
            else:
                return self.__scores[state]

        return None

    def __minimax(self, board, depth, minimize):
        end_state = self.__check_state(board)
        if end_state:
            return self.__evaluation(end_state, depth)
             
        if minimize:
            best_score = -math.inf
            for i in range(len(board)):
                for j in range(len(board[0])):
                    # create a new node
                    if board[i][j] == -1:
                        # try puting chess
                        board[i][j] = self.__ai_chess
                        # Calculating score of this case
                        score = self.__minimax(board, depth+1, False)
                        # restore
                        board[i][j] = -1
                        best_score = max(best_score, score)
            
            return best_score
        else:
            best_score = math.inf
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == -1:
                        board[i][j] = self.__human_chess
                        score = self.__minimax(board, depth+1, True)
                        board[i][j] = -1
                        best_score = min(best_score, score)
                        
            return best_score

    def __alpha_beta_pruning(self, board, depth, minimize, alpha, beta):
        # if this state is end of the board then return utility value
        end_state = self.__check_state(board)
        if end_state:
            return self.__evaluation(end_state, depth)

        if minimize:
            best_score = -math.inf
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == -1:
                        board[i][j] = self.__ai_chess
                        score = self.__alpha_beta_pruning(board, depth + 1, not minimize, alpha, beta)
                        board[i][j] = -1

                        alpha = max(alpha, score)
                        best_score = max(alpha, best_score)
                        if beta <= alpha:
                            return best_score
            return best_score
        else:
            best_score = math.inf
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == -1:
                        board[i][j] = self.__human_chess
                        score = self.__alpha_beta_pruning(board, depth + 1, not minimize, alpha, beta)
                        board[i][j] = -1

                        beta = min(beta, score)
                        best_score = min(beta, best_score)
                        if beta <= alpha:
                            return best_score
            return best_score

    def __is_new_board(self, board):
        count = 0
        for row in board:
            count += row.count(-1)
        return count == len(board)*len(board[0])
        
    def __best_move(self, chess):
        best_score = -math.inf
        board = self.__table
        position = [0, 0]
        if self.__is_new_board(board):
            # position = [0, 0]
            position = [random.randrange(0, len(board)), random.randrange(0, len(board[0]))]
        else:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == -1:
                        board[i][j] = chess
                        score = self.__alpha_beta_pruning(board, 0, False, -math.inf, math.inf)
                        board[i][j] = -1
                        if score > best_score:
                            best_score = score
                            position = (i, j)

        self.put_to_possition(position[0], position[1], chess)

    def ai(self, chess):
        self.__best_move(chess)