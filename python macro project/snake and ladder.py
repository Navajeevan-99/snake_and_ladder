import random

snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}


def roll_dice():
    return random.randint(1, 6)

def move_player(player, current_position):
    input(f"{player}, press Enter to roll the dice...")
    dice_value = roll_dice()
    print(f"{player} rolled a {dice_value}")
    current_position += dice_value

    if current_position in snakes:
        print(f"Oops! {player} got bitten by a snake and moved from {current_position} to {snakes[current_position]}")
        current_position = snakes[current_position]
    elif current_position in ladders:
        print(f"Yay! {player} climbed a ladder from {current_position} to {ladders[current_position]}")
        current_position = ladders[current_position]

    print(f"{player} is now on position {current_position}")
    return current_position

def play_game():
    player1 = "Player 1"
    player2 = "Player 2"
    player1_position = 0
    player2_position = 0

    while True:
        player1_position = move_player(player1, player1_position)
        if player1_position >= 100:
            print(f"{player1} wins!")
            break

        player2_position = move_player(player2, player2_position)
        if player2_position >= 100:
            print(f"{player2} wins!")
            break

play_game()
