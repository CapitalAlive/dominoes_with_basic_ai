import random


def pop_a_piece(main_deck, cards_amount):
    return [main_deck.pop(random.randint(0, len(main_deck) - 1)) for _ in range(cards_amount)]

def computer_ai(pieces_list, snake):
    basic_numbers = {x:0 for x in range(0, 7)}
    for number in basic_numbers:
        number_in_snake_count = sum([sublist.count(number) for sublist in snake])
        number_in_piece_list = sum([sublist.count(number) for sublist in pieces_list])
        total_apparitions = number_in_snake_count + number_in_piece_list
        basic_numbers[number] = total_apparitions
    piece_score_list = []
    for piece in pieces_list:
        piece_score = basic_numbers[piece[0]] + basic_numbers[piece[1]]
        piece_score_list.append([piece, piece_score])
    piece_score_list.sort()
    piece_score_list = [x[0] for x in piece_score_list]
    for piece in piece_score_list:
        if snake[0][0] in piece:
            next_move = -(pieces_list.index(piece) + 1)
            return next_move
        elif snake[-1][1] in piece:
            next_move = pieces_list.index(piece) + 1
            return next_move
    next_move = 0
    return next_move

def game_start():
    while True:
        full_deck = [[n, second_n] for n in range(0, 7) for second_n in range(n, 7)]
        stock_pieces = pop_a_piece(full_deck, 14)
        computer_pieces = pop_a_piece(full_deck, 7)
        player_pieces = pop_a_piece(full_deck, 7)
        for n in range(6, -1, -1):
            snake = [[n, n]]
            if snake[0] in computer_pieces:
                computer_pieces.remove([n, n])
                status = "player"
                return stock_pieces, computer_pieces, player_pieces, snake, status
            elif snake[0] in player_pieces:
                player_pieces.remove([n, n])
                status = "computer"
                return stock_pieces, computer_pieces, player_pieces, snake, status


def print_table(stock_pieces, computer_pieces, snake, player_pieces):
    print("======================================================================")
    print(f"Stock size: {len(stock_pieces)}")
    print(f"Computer pieces: {len(computer_pieces)}\n")
    if len(snake) <= 6:
        print(', '.join(map(str, snake)))
    else:
        print(', '.join(map(str, snake[:3])), "...", ', '.join(map(str, snake[-3:])))
    print("\nYour pieces:")
    for x in range(len(player_pieces)):
        print(str(x + 1) + ":" + str(player_pieces[x]))
    print("\nStatus: ", end=" ")


def next_move_validation(status, pieces_list, snake):
    while True:
        try:
            if status == "player":
                next_move = float(input())
            elif status == "computer":
                next_move = random.randint(-len(pieces_list), len(pieces_list))
            if next_move % 1 == 0 and abs(next_move) <= len(pieces_list):
                next_move = int(next_move)
                for n in pieces_list[abs(next_move) - 1]:
                    if next_move < 0:
                        if n == snake[0][0]:
                            return next_move
                    elif next_move > 0:
                        if n == snake[-1][1]:
                            return next_move
                    elif next_move == 0:
                        return next_move
                if status == "player":
                    print("Illegal move. Please try again.")
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")


def piece_flipper(piece):
    piece = [piece[1], piece[0]]
    return piece


def run_the_move(status, next_move, snake, pieces_list, stock_pieces):
    if next_move > 0:
        if pieces_list[abs(next_move) - 1][0] == snake[-1][1]:
            snake.append(pieces_list.pop(next_move - 1))
        else:
            snake.append(piece_flipper(pieces_list.pop(next_move - 1)))
    elif next_move < 0:
        if pieces_list[abs(next_move) - 1][1] == snake[0][0]:
            snake.insert(0, pieces_list.pop(abs(next_move) - 1))
        else:
            snake.insert(0, piece_flipper(pieces_list.pop(abs(next_move) - 1)))
    elif next_move == 0:
        if stock_pieces:
            pieces_list.append(stock_pieces.pop(0))
    if status == "player":
        status = "computer"
    elif status == "computer":
        status = "player"
    return status, snake, pieces_list, stock_pieces


def game_status_checker(player_pieces, computer_pieces, stock_pieces, snake):
    if not player_pieces:
        print("The game is over. You won!")
        return True
    elif not computer_pieces:
        print("The game is over. The computer won!")
        return True
    elif snake[0][0] == snake[-1][1]:
        count = sum(sublist.count(snake[0][0]) for sublist in snake)
        if count == 8:
            print("Status: The game is over. It's a draw!")
            return True
    possible_plays = 0
    if not stock_pieces:
        for side_of_snake in [snake[0][0], snake[-1][1]]:
            for piece in player_pieces + computer_pieces:
                if side_of_snake in piece:
                    possible_plays += 1
                    break
        if possible_plays == 0:
            print("Status: The game is over. It's a draw!")
            return True



    if status == "player":
        print("It's your turn to make a move. Enter your command.")
    elif status == "computer":
        print("Computer is about to make a move. Press Enter to continue...")
        input()


stock_pieces, computer_pieces, player_pieces, snake, status = game_start()

while True:
    print_table(stock_pieces, computer_pieces, snake, player_pieces)
    game_over = game_status_checker(player_pieces, computer_pieces, stock_pieces, snake)
    if game_over is True:
        break
    if status == "player":
        next_move = next_move_validation(status, player_pieces, snake)
        status, snake, pieces_list, stock_pieces = run_the_move(status, next_move, snake, player_pieces, stock_pieces)
    elif status == "computer":
        next_move = computer_ai(computer_pieces, snake)
        status, snake, pieces_list, stock_pieces = run_the_move(status, next_move, snake, computer_pieces, stock_pieces)
