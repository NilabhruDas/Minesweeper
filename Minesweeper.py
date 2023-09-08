import tkinter as tk
import random

class Minesweeper:
    def __init__(self, master, rows, cols, mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.game_over = False

        self.create_board()
        self.place_mines()
        self.calculate_numbers()

    def create_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(
                    self.master,
                    width=2,
                    height=1,
                    font=("Arial", 12),
                    command=lambda r=row, c=col: self.click(r, c),
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col] == 0:
                self.board[row][col] = -1
                mines_placed += 1

    def calculate_numbers(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    continue
                neighbors = self.get_neighbors(row, col)
                mine_count = sum(1 for r, c in neighbors if self.is_mine(r, c))
                self.board[row][col] = mine_count

    def get_neighbors(self, row, col):
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    neighbors.append((r, c))
        return neighbors

    def is_mine(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.board[row][col] == -1

    def click(self, row, col):
        if self.game_over or self.buttons[row][col]['state'] == 'disabled':
            return

        if self.board[row][col] == -1:
            self.game_over = True
            self.buttons[row][col].config(text="💣", background="red")
            self.reveal_board("Game Over", "red")
            return

        self.buttons[row][col].config(text=str(self.board[row][col]), state='disabled')

        if self.check_win():
            self.reveal_board("You Win!", "green")

        if self.board[row][col] == 0:
            neighbors = self.get_neighbors(row, col)
            for r, c in neighbors:
                self.click(r, c)

    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != -1 and self.buttons[row][col]['state'] != 'disabled':
                    return False
        return True

    def reveal_board(self, message, color):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    self.buttons[row][col].config(text="💣", background=color)
                else:
                    self.buttons[row][col].config(text=str(self.board[row][col]))
                self.buttons[row][col].config(state='disabled')

        result_label = tk.Label(
            self.master,
            text=message,
            font=("Arial", 20,"bold"),
            fg=color,
        )
        result_label.grid(row=self.rows, columnspan=self.cols)

def main():
    root = tk.Tk()
    root.title("Minesweeper")
    rows = 10
    cols = 10
    mines = 15
    game = Minesweeper(root, rows, cols, mines)
    root.mainloop()

if __name__ == "__main__":
    main()
