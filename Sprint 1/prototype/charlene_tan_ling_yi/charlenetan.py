import tkinter as tk
from tkinter import messagebox
import random

class Worker:
    MOVE = 0
    BUILD = 1

    def __init__(self, player_id):
        self.player_id = player_id
        self.position = [random.randint(0, 4), random.randint(0, 4)]
        self.action = Worker.MOVE
    
    def get_position(self):
        return self.position
    
    def get_action(self):
        return self.action
    
    def set_position(self, position):
        self.position = position
        
    def set_action(self, action):
        self.action = Worker.BUILD if self.action == Worker.MOVE else Worker.MOVE

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(5)] for _ in range(5)]
        
class SantoriniGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Santorini")
        self.window.geometry("400x400")
        self.window.configure(bg="#fffff0")
        
        self.board = Board()
        self.worker = Worker(player_id=1)
        
        self.buttons = []
        self.board_frame = None
        
        self.create_board()
        self.initialize_worker()
        
        self.window.mainloop()
    
    def create_board(self):
        self.board_frame = tk.Frame(self.window, bg="#b7d3bd", padx=20, pady=20)
        self.board_frame.pack(pady=15)
        
        for row in range(5):
            button_row = []
            for col in range(5):
                btn = tk.Button(self.board_frame, width=4, height=2, bg="green", command=lambda r=row, c=col: self.handle_cell_click(r, c))
                btn.grid(row=row, column=col, padx=2, pady=2)
                button_row.append(btn)
            self.buttons.append(button_row)
        
    def initialize_worker(self):
        row, col = self.worker.get_position()
        self.buttons[row][col].config(bg="grey", text="W", fg="black")
        
    def handle_cell_click(self, row, col):
        print("Active")
            
if __name__ == "__main__":
    game = SantoriniGame()
