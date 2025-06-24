import tkinter as tk
from tkinter import messagebox

class SantoriniPrototypeGame:
    def __init__(self):
        self.board_size = 5  # 5x5 board
        self.cell_size = 100  # 100x100 pixels
        
        # Board levels:
        # 0, 1, 2: normal levels,
        # 3: winning level (tower of height 3)
        # 4: dome built (blocks movement)
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        
        # Set initial person position and phase ("move" or "build")
        self.person_pos = (2, 2)
        self.phase = "move"
        self.game_over = False

        self.window = tk.Tk()
        self.window.title("Santorini Prototype Game")
        self.window.resizable(False, False)
        self.canvas = tk.Canvas(
            self.window,
            width=self.board_size * self.cell_size,
            height=self.board_size * self.cell_size,
            bg="lightblue"
        )
        self.canvas.pack()
        
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.redraw()
        self.window.mainloop()
        
    def redraw(self):
        self.canvas.delete("all")
        self.draw_board()
        
        if self.phase == "move":
            for (r, c) in self.get_valid_moves():
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="green", width=3, dash=(4,2))
        elif self.phase == "build":
            for (r, c) in self.get_valid_builds():
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="orange", width=3, dash=(4,2))
        
        self.draw_person()
        self.canvas.create_text(10, 10, anchor="nw", text="Phase: " + self.phase, font=("Arial", 16), fill="blue")
    
    def draw_board(self):
        # Draw plain board with white cells and black outlines
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                height = self.board[row][col]
                if height > 0:
                    text = "Dome" if height == 4 else str(height)
                    self.canvas.create_text(
                        x1 + self.cell_size/2,
                        y1 + self.cell_size/2,
                        text=text,
                        font=("Arial", 20),
                        fill="black"
                    )
        
    def draw_person(self):
        row, col = self.person_pos
        x_center = col * self.cell_size + self.cell_size / 2
        y_center = row * self.cell_size + self.cell_size / 2
        radius = self.cell_size / 3
        self.canvas.create_oval(
            x_center - radius, y_center - radius,
            x_center + radius, y_center + radius,
            fill="gray", outline="black", width=2
        )
        
    def get_valid_moves(self):
        valid = []
        pr, pc = self.person_pos
        for r in range(pr - 1, pr + 2):
            for c in range(pc - 1, pc + 2):
                if (r, c) == self.person_pos:
                    continue
                if 0 <= r < self.board_size and 0 <= c < self.board_size:
                    if self.board[r][c] == 4:  # Dome blocks movement
                        continue
                    valid.append((r, c))
        return valid
    
    def get_valid_builds(self):
        valid = []
        pr, pc = self.person_pos
        for r in range(pr - 1, pr + 2):
            for c in range(pc - 1, pc + 2):
                if (r, c) == self.person_pos:
                    continue
                if 0 <= r < self.board_size and 0 <= c < self.board_size:
                    # Allow building if cell level is less than 3 or if it's exactly 3 (to build a dome)
                    if self.board[r][c] < 3 or self.board[r][c] == 3:
                        valid.append((r, c))
        return valid
    
    def on_canvas_click(self, event):
        if self.game_over:
            return
        
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return
        
        if self.phase == "move":
            if (row, col) in self.get_valid_moves():
                self.person_pos = (row, col)
                # Win condition: if the worker moves onto a cell with level 3, they win.
                if self.board[row][col] == 3:
                    self.redraw()
                    messagebox.showinfo("Victory!", "You win by reaching a tower of level 3!")
                    self.game_over = True
                    return
                self.phase = "build"
            else:
                messagebox.showinfo("Invalid Move", "Select a valid adjacent cell to move.")
        elif self.phase == "build":
            if (row, col) in self.get_valid_builds():
                if self.board[row][col] < 3:
                    self.board[row][col] += 1
                elif self.board[row][col] == 3:
                    self.board[row][col] = 4  # Build dome on a level 3 cell
                self.phase = "move"
            else:
                messagebox.showinfo("Invalid Build", "Select a valid adjacent cell to build.")
        self.redraw()

if __name__ == "__main__":
    SantoriniPrototypeGame()