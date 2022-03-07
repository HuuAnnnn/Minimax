import time
from Caro import Caro
import random

def user_ai(init):
    chess = 1
    while True:
        try:
            if chess == 0:
                print(f"Turn of {chess}: ", end="")
                x_y_pos = input()
                if x_y_pos.strip().lower() == 'sur':
                    break

                x_y_pos = x_y_pos.strip()
                x_pos, y_pos = tuple(x_y_pos.split(" "))

                if not init.put_to_possition(int(x_pos), int(y_pos), chess):
                    print("Enter again")
                    continue
            else:
                start = time.time()
                init.ai(chess)
                end = time.time()
                print(f"Evaluation {round(end - start, 7)}")

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

def user_input(init: Caro, chess):
    print(f"Turn of {chess}: ", end="")
    x_y_pos = input()
    x_y_pos = x_y_pos.strip()
    x_pos, y_pos = tuple(x_y_pos.split(" "))

    return init.put_to_possition(int(x_pos), int(y_pos), chess)
    
def user_user(init):
    chess = 1
    while True:
        try:
            if chess == 0:
                state_user1 = user_input(init, chess)
                if not state_user1:
                    print("Enter again")
                    continue
            else:
                state_user2 = user_input(init, chess)

                if not state_user2:
                    print("Enter again")
                    continue

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

if __name__ == '__main__':
    input_size = input("Size of board: ")
    size = 3
    if input_size.isdigit() and int(input_size) <= 8: 
        size = int(input_size)


    user_ai(Caro(size))
