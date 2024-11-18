import tkinter as tk
import random


class SnakeAndLadderGame:
    def __init__(self):  # Fixed constructor name
        self.window = tk.Tk()
        self.window.title("Snake and Ladder")
        self.players = []
        self.num_players = 2
        self.player_positions = []
        self.current_player = 0
        self.player_started = []
        self.colors = ["red", "blue", "green", "yellow"]  # Player colors
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 87: 24, 93: 73, 98: 78}
        self.ladders = {3: 22, 8: 26, 20: 29, 28: 55, 50: 91, 57: 96, 72: 94}
        self.create_setup_ui()

    def create_setup_ui(self):
        tk.Label(self.window, text="Snake and Ladder Game", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.window, text="Select Number of Players (2-4):").pack()

        self.player_choice = tk.IntVar(value=2)
        for i in range(2, 5):
            tk.Radiobutton(self.window, text=f"{i} Players", variable=self.player_choice, value=i).pack()

        tk.Button(self.window, text="Start Game", command=self.start_game).pack(pady=10)

    def start_game(self):
        self.num_players = self.player_choice.get()
        self.players = [f"Player {i + 1}" for i in range(self.num_players)]
        self.player_positions = [0] * self.num_players
        self.player_started = [False] * self.num_players  # Track if players have rolled a 1
        self.current_player = 0
        self.create_game_ui()

    def create_game_ui(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.info_label = tk.Label(self.window, text=f"{self.players[self.current_player]}'s turn", font=("Helvetica", 14))
        self.info_label.pack(pady=10)

        self.dice_label = tk.Label(self.window, text="Roll the Dice!", font=("Helvetica", 12))
        self.dice_label.pack(pady=10)

        tk.Button(self.window, text="Roll Dice", command=self.roll_dice).pack(pady=10)
        self.board_canvas = tk.Canvas(self.window, width=400, height=400, bg="white")
        self.board_canvas.pack(pady=20)
        self.results_label = tk.Label(self.window, text="", font=("Helvetica", 12), fg="green")
        self.results_label.pack(pady=10)  # Results label placed below the board
        self.draw_board()
        self.update_player_positions()

    def draw_board(self):
        self.board_canvas.delete("all")
        size = 10  # 10x10 board
        cell_size = 40

        # Draw grid
        for row in range(size):
            for col in range(size):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                self.board_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                num = 100 - (row * 10 + col) if row % 2 == 0 else 100 - (row * 10 + (9 - col))
                self.board_canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(num), font=("Arial", 8))

        # Draw snakes
        for start, end in self.snakes.items():
            self.draw_snake_or_ladder(start, end, "red")

        # Draw ladders
        for start, end in self.ladders.items():
            self.draw_snake_or_ladder(start, end, "green")

    def draw_snake_or_ladder(self, start, end, color):
        def get_coords(pos):
            row, col = divmod(pos - 1, 10)
            if (row % 2) == 0:
                col = col
            else:
                col = 9 - col
            x = col * 40 + 20
            y = (9 - row) * 40 + 20
            return x, y

        x1, y1 = get_coords(start)
        x2, y2 = get_coords(end)
        self.board_canvas.create_line(x1, y1, x2, y2, fill=color, width=2, arrow=tk.LAST)

    def roll_dice(self):
        dice_roll = random.randint(1, 6)
        current_player_name = self.players[self.current_player]

        self.dice_label.config(text=f"{current_player_name} rolled a {dice_roll}!")

        if not self.player_started[self.current_player]:
            if dice_roll == 1:
                self.player_started[self.current_player] = True
                self.info_label.config(text=f"{current_player_name} has entered the game!")
            else:
                self.info_label.config(text=f"{current_player_name} needs to roll a 1 to start!")
                self.next_turn()
                return

        current_position = self.player_positions[self.current_player]
        new_position = current_position + dice_roll

        if new_position in self.snakes:
            new_position = self.snakes[new_position]
            self.info_label.config(text=f"{current_player_name} got bitten by a snake!")
        elif new_position in self.ladders:
            new_position = self.ladders[new_position]
            self.info_label.config(text=f"{current_player_name} climbed a ladder!")

        if new_position <= 100:
            self.player_positions[self.current_player] = new_position

        self.update_player_positions()

        if new_position == 100:
            self.info_label.config(text=f"🎉 {current_player_name} wins! 🎉")
            self.player_positions[self.current_player] = 101  # Mark as finished

        self.next_turn()

    def next_turn(self):
        active_players = [pos for pos in self.player_positions if pos < 100]
        if len(active_players) == 0:  # Game Over
            results = sorted(zip(self.players, self.player_positions), key=lambda x: x[1], reverse=True)
            result_text = f"Winner: {results[0][0]}\nRunner-up: {results[1][0]}"
            self.results_label.config(text=result_text)
            return

        self.current_player = (self.current_player + 1) % self.num_players
        while self.player_positions[self.current_player] > 100:  # Skip finished players
            self.current_player = (self.current_player + 1) % self.num_players

        self.info_label.config(text=f"{self.players[self.current_player]}'s turn")

    def update_player_positions(self):
        self.draw_board()
        for i, pos in enumerate(self.player_positions):
            if pos <= 100:
                row, col = divmod(pos - 1, 10)
                col = col if row % 2 == 0 else 9 - col
                x = col * 40 + 20
                y = (9 - row) * 40 + 20
                self.board_canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=self.colors[i])

    def run(self):
        self.window.mainloop()


# Run the game
game = SnakeAndLadderGame()
game.run()
