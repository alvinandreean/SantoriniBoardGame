import tkinter as tk

GRID_SIZE = 5
CELL_SIZE = 100

class Block:
    def __init__(self, level=0):
        self.level = level

class Tile:
    def __init__(self):
        self.worker = None
        self.building = Block()

class Worker:
    def __init__(self, player, row, col):
        self.player = player  # "P1" or "P2"
        self.row = row
        self.col = col

class Board:
    def __init__(self):
        self.board = [[Tile() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Create 2 workers per player
        self.workers = {
            "P1": [Worker("P1", 0, 0), Worker("P1", 0, 1)],
            "P2": [Worker("P2", 4, 4), Worker("P2", 4, 3)],
        }

        # Place them on the board
        for player_workers in self.workers.values():
            for worker in player_workers:
                self.board[worker.row][worker.col].worker = worker

class Game:
    def __init__(self, root):
        self.root = root
        self.board = Board()
        self.current_player = "P1"
        self.selected_worker = None

        # Setup UI
        self.canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
        self.canvas.pack()
        self.status = tk.Label(root, text=f"{self.current_player}'s turn: Select a worker")
        self.status.pack()

        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

                # Draw tile background based on level
                level = self.board.board[row][col].building.level
                color = ["white", "lightblue", "skyblue", "blue", "gray"][level]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                # Draw worker if present
                worker = self.board.board[row][col].worker
                if worker:
                    fill_color = "red" if worker.player == "P1" else "green"
                    self.canvas.create_oval(x1+20, y1+20, x2-20, y2-20, fill=fill_color)

    def on_click(self, event):
        row, col = event.y // CELL_SIZE, event.x // CELL_SIZE

        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return  # Click out of bounds

        clicked_tile = self.board.board[row][col]

        if self.selected_worker is None:
            # Select your own worker
            if clicked_tile.worker and clicked_tile.worker.player == self.current_player:
                self.selected_worker = clicked_tile.worker
                self.status.config(text=f"{self.current_player}: Selected worker at ({row}, {col}) - Click to move")
        else:
            # Try to move
            sw = self.selected_worker
            if self.is_valid_move(sw.row, sw.col, row, col):
                # Update tile references
                self.board.board[sw.row][sw.col].worker = None
                sw.row, sw.col = row, col
                self.board.board[row][col].worker = sw

                self.selected_worker = None
                self.switch_player()
            else:
                self.status.config(text="Invalid move. Try again.")
        
        self.draw_board()

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        if abs(from_row - to_row) > 1 or abs(from_col - to_col) > 1:
            return False  # Too far

        target_tile = self.board.board[to_row][to_col]
        if target_tile.worker:
            return False  # Occupied

        from_level = self.board.board[from_row][from_col].building.level
        to_level = target_tile.building.level
        if to_level > from_level + 1:
            return False  # Can't climb more than 1 level

        if to_level == 4:
            return False  # Can't move onto a dome

        return True

    def switch_player(self):
        self.current_player = "P1" if self.current_player == "P2" else "P2"
        self.status.config(text=f"{self.current_player}'s turn: Select a worker")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Santorini - Prototype")
    game = Game(root)
    root.mainloop()
