from Caro import CaroBoardGame

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