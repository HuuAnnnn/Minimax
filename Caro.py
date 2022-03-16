import math
import random
import numpy as np

class Caro:
    __table_size = 3
    __table = []
    __human_chess = 0
    __ai_chess = 1
    __scores = {"Win": 10, "Lose": -10, "Draw": 0}
    __chess_value = {0: 'O', 1: 'X'}
    __win_goal = 3

    def __init__(self, size: int) -> None:
        self.__table_size = size
        self.__table = [[-1 for i in range(self.__table_size)] for j in range(self.__table_size)]

    def get_table(self):
        return self.__table

    def put_to_possition(self, x_pos: int, y_pos: int, chess: int):
        try:
            if self.__table[x_pos][y_pos] == -1:
                self.__table[x_pos][y_pos] = chess
                return True
            else:
                return False
        except:
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
            count_x = 0
            count_o = 0
            for j in range(len(board[0])):

                if board[i][j] == 1:
                    if count_o < self.__win_goal:
                        count_o = 0
                    count_x += 1

                if board[i][j] == 0:
                    if count_x < self.__win_goal:
                        count_x = 0
                    count_o += 1
                
                if board[i][j] == -1:
                    if count_o < self.__win_goal:
                        count_o = 0
                    if count_x < self.__win_goal:
                        count_x = 0

            if count_x == self.__win_goal or count_o == self.__win_goal:
                return (count_x, count_o)

        return None

    def __check_columns(self, board):
        for i in range(len(board)):
            count_x = 0
            count_o = 0
            for j in range(len(board[0])):

                if board[j][i] == 1:
                    if count_o < self.__win_goal:
                        count_o = 0

                    count_x += 1
                
                elif board[j][i] == 0:
                    if count_x < self.__win_goal:
                        count_x = 0

                    count_o+=1
                
                elif board[i][j] == -1:
                    if count_o < self.__win_goal:
                        count_o = 0
                    if count_x < self.__win_goal:
                        count_x = 0

            if count_x == self.__win_goal or count_o == self.__win_goal:
                return (count_x, count_o)
                
        return None
    
    def __count_in_diagonal(self, row):
        count_x = 0
        count_o = 0
        for cell in row:
            if cell == 1:
                if count_o < self.__win_goal:
                    count_o = 0
                count_x += 1
            if cell == 0:
                if count_x < self.__win_goal:
                    count_x = 0
                count_o+=1

            if cell == -1:
                if count_o < self.__win_goal:
                    count_o = 0
                if count_x < self.__win_goal:
                    count_x = 0

        return (count_x, count_o)

    def __check_diagonal(self, board):
        count_x = 0
        count_o = 0
        np_board = np.array(board)
        for i in range(-len(np_board)+1, len(np_board)):
            board_diagonal = list(np_board.diagonal(i))
            count_x, count_o = self.__count_in_diagonal(board_diagonal)
            
            if count_x == self.__win_goal or count_o == self.__win_goal:
                return (count_x, count_o)

        return None
        
    def __check_anti_diagonal(self, board):
        count_x = 0
        count_o = 0
        np_board = np.fliplr(np.array(board))
        for i in range(-len(np_board)+1, len(np_board)):
            board_diagonal = list(np_board.diagonal(i))
            count_x, count_o = self.__count_in_diagonal(board_diagonal)
            
            if count_x == self.__win_goal or count_o == self.__win_goal:
                return (count_x, count_o)

        return None
        
    def __winner(self, board):
        states = [
            self.__check_rows(board),
            self.__check_columns(board),
            self.__check_diagonal(board),
            self.__check_anti_diagonal(board)
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

    def __get_possible_move(self, board):
        return list(zip(*np.where(np.array(board) == -1)))

    def __minimax(self, board, depth, minimize):
        end_state = self.__check_state(board)
        if end_state:
            return self.__evaluation(end_state, depth)
             
        if minimize:
            possible_move = self.__get_possible_move(board)
            best_score = -math.inf
            for move in possible_move:
                x, y = move
                board[x][y] = self.__ai_chess
                # Calculating score of this case
                score = self.__minimax(board, depth+1, False)
                # restore
                board[x][y] = -1
                best_score = max(best_score, score)
    
            return best_score
        else:
            possible_move = self.__get_possible_move(board)
            best_score = math.inf
            for move in possible_move:
                x, y = move
                board[x][y] = self.__human_chess
                # Calculating score of this case
                score = self.__minimax(board, depth+1, True)
                # restore
                board[x][y] = -1
                best_score = min(best_score, score)
                        
            return best_score

    def __alpha_beta_pruning(self, board, depth, minimize, alpha, beta):
        # if this state is end of the board then return utility value
        end_state = self.__check_state(board)
        if end_state:
            return self.__evaluation(end_state, depth)

        if minimize:
            possible_move = self.__get_possible_move(board)
            best_score = -math.inf
            for move in possible_move:
                x, y = move
                board[x][y] = self.__ai_chess
                score = self.__alpha_beta_pruning(board, depth + 1, not minimize, alpha, beta)
                board[x][y] = -1

                alpha = max(alpha, score)
                best_score = max(alpha, best_score)
                if beta <= alpha:
                    break

            return best_score
        else:
            possible_move = self.__get_possible_move(board)
            best_score = math.inf
            for move in possible_move:
                x, y = move
                board[x][y] = self.__human_chess
                score = self.__alpha_beta_pruning(board, depth + 1, not minimize, alpha, beta)
                board[x][y] = -1

                beta = min(beta, score)
                best_score = min(beta, best_score)
                if beta <= alpha:
                    break

            return best_score

    def __is_new_board(self, board):
        count = 0
        for row in board:
            count += row.count(-1)
        return count == len(board)*len(board[0])

    def __is_empty(self, board, x, y):
        try:
            return board[x][y] != -1
        except:
            return False
    def __best_move(self, chess):
        best_score = -math.inf
        board = self.__table
        position = [0, 0]
        human_chess_pos = list(zip(*np.where(np.array(board) == 0)))

        if self.__is_new_board(board):
            position = [random.randrange(0, len(board)), random.randrange(0, len(board[0]))]
        elif human_chess_pos and len(human_chess_pos)  == 1:
            i = 0
            x = human_chess_pos[0][0]
            y = human_chess_pos[0][1]
            empty_cell = self.__get_possible_move(board)
            possible_move = [(x, y), (x-1, y), (x+1, y), (x, y+1), (x, y-1), (x-1, y+1), (x-1, y-1), (x+1, y+1), (x+1, y-1)]
            x_pos, y_pos = random.choice(possible_move)
            while True:
                if empty_cell[x_pos][y_pos] != -1:
                    board[x_pos][y_pos] = self.__ai_chess
                    break

            
        else:
            possible_move = self.__get_possible_move(board)
            for move in possible_move:
                x, y = move
                board[x][y] = chess
                score = self.__alpha_beta_pruning(board, 0, False, -math.inf, math.inf)
                board[x][y] = -1
                if score > best_score:
                    best_score = score
                    position = (x, y)

        self.put_to_possition(position[0], position[1], chess)

    def ai(self, chess):
        self.__best_move(chess)