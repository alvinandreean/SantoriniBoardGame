import tkinter as tk
from tkinter import messagebox

class Worker:
    def __init__(self, player_id):
        """ 
        Worker class to represent a worker in the game.
        """
        self.player_id = player_id
        self.position = [2, 2]  # Start in the center of the board
        self.action = "move"  # "move" or "build"
        
    def get_position(self):
        return self.position
    
    def get_action(self):
        return self.action
    
    def set_position(self, position):
        self.position = position
        
    def set_action(self, action):
        if self.action == "move":
            self.action = "build"
        else:
            self.action = "move"
            
class Board:
    """ 
    Board class to represent the game board.
    """
    def __init__(self):
        self.grid = [[0 for _ in range(5)] for _ in range(5)]  # 5x5 board, used for storing tower heights
        
    def get_cell(self, row, col):
        return self.grid[row][col]
    
    def set_cell(self, row, col, value):
        self.grid[row][col] = value
        
    def is_valid_move(self, current_pos, new_pos):
        current_row, current_col = current_pos
        new_row, new_col = new_pos
        
        # Check if the clicked cell is adjacent (horizontally, vertically, or diagonally)
        if abs(new_row - current_row) > 1 or abs(new_col - current_col) > 1:
            return False
        
        return True
    
    def has_dome(self, row, col):
        return self.grid[row][col] == 4
    
    def check_win(self, row, col):
        return self.grid[row][col] == 3
        
        
class SantoriniGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Santorini Prototype")
        self.window.geometry("500x500")
        self.window.configure(bg="#E0F7FA")
        
        # Board variables
        self.board = Board()
        self.worker = Worker(player_id=1)
        
        self.buttons = []
        self.board_frame = None
        
        self.create_board()

        self.initialize_worker()
        # Start the main loop
        self.window.mainloop()
    
    def create_board(self):
        # Create a frame for the board
        self.board_frame = tk.Frame(
            self.window,
            bg="#81D4FA",
            padx=10,
            pady=10
        )
        self.board_frame.pack(pady=15)
        
        # Create the 5x5 grid of buttons
        
        for row in range(5):
            button_row = []
            for col in range(5):
                # Create a button for each cell with a command to handle the cell click
                btn = tk.Button(
                    self.board_frame,
                    width=6,
                    height=3,
                    bg="white",
                    command=lambda r=row, c=col: self.handle_cell_click(r, c)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                button_row.append(btn)
            self.buttons.append(button_row)
        
    def initialize_worker(self):
        row, col = self.worker.get_position()
        self.buttons[row][col].config(bg="grey", text="W", fg="white")
        
    def handle_cell_click(self, row, col):
        """Handle a click on a cell based on the current action"""
        if self.worker.get_action() == "move":
            self.move_to(row, col)
        else:  # build action
            self.build_tower(row, col)
    
    def move_to(self, row, col):
        current_row, current_col = self.worker.get_position() # Get current worker position
        
        # Check if the clicked cell is valid to move to
        if self.is_valid_action(row, col):
            
            if self.board.has_dome(row, col):
                messagebox.showinfo("Invalid Move", "You cannot move to a cell with a dome")
                return
            
            # Clear the current worker position but preserve the tower height
            current_height = self.board.get_cell(current_row, current_col)
            
            if current_height > 0:
                height_text = str(current_height) 
            else:
                height_text = ""
                
            self.buttons[current_row][current_col].config(bg="white", text=height_text, fg="black")
            
            # Move worker to the new position
            self.worker.set_position([row, col])
            new_position_height = self.board.get_cell(row, col)
            
            
            if self.board.check_win(row, col): # Win condition, when the worker reaches a tower of height 3
                self.buttons[row][col].config(bg="grey", text=f"W({new_position_height})", fg="white")
                messagebox.showinfo("Game Over", "You win!")
                self.window.quit()
            elif new_position_height > 0 and new_position_height < 3:
                # Show both worker and height if there's a tower
                self.buttons[row][col].config(bg="grey", text=f"W({new_position_height})", fg="white")
            else:
                # Just show worker if there's no tower
                self.buttons[row][col].config(bg="grey", text="W", fg="white")
            
            # Switch to build action
            self.worker.set_action("build")
            
        else:
            messagebox.showinfo("Invalid Move", "You can only move to adjacent cells")
    
    def is_valid_action(self, row, col):
        
        # Get the current position
        current_row, current_col = self.worker.get_position()
        
        # Check if we're clicking on the current position
        if row == current_row and col == current_col:
            return False
        
        # Check if the clicked cell is adjacent (horizontally, vertically, or diagonally)
        if abs(row - current_row) > 1 or abs(col - current_col) > 1:
            return False
        
        return True
    
    
    def build_tower(self, row, col):
        
        if self.is_valid_action(row, col):
            
            if self.board.has_dome(row, col):
                messagebox.showinfo("Invalid Build", "You cannot build on a cell with a dome")
                return
            
            # Build tower (increase height by 1)
            current_height = self.board.get_cell(row, col)
            new_height = current_height + 1
            self.board.set_cell(row, col, new_height)
            
            
            # Update the button to show the new height
            if new_height == 4:
                self.buttons[row][col].config(bg="blue", text="D", fg="white")
            else:
                self.buttons[row][col].config(bg="grey", text=str(new_height), fg="white")
                self.worker.set_action("move")  # Switch back to move action after building
        else:
            messagebox.showinfo("Invalid Build", "You can only build on adjacent cells")
            
        
if __name__ == "__main__":
    game = SantoriniGame()
    
