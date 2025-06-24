import tkinter as tk
import tkinter.messagebox as messagebox
import os
import sys

from colors.color import Color
from game import Game
from player import Player
from position import Position


class SantoriniApp:
    """Main application class for Santorini game."""
    
    # Constants
    TILE    = 150
    BOARD_W = 5
    BOARD_H = 5

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the main application."""
        self._root = root
        root.title("Santorini")
        root.geometry("1400x1000")        
        root.update_idletasks()           
        w = root.winfo_width()
        h = root.winfo_height()
        x = (root.winfo_screenwidth()  - w) // 2
        y = (root.winfo_screenheight() - h) // 2
        root.geometry(f"{w}x{h}+{x}+{y}")       # Center the window on the screen

        self._game = None
        self._rect_ids = {}
        self._selected_worker_pos = None

        # UI variables
        self._player1_name_var  = tk.StringVar()
        self._player2_name_var  = tk.StringVar()
        self._player1_color_var = tk.StringVar()
        self._player2_color_var = tk.StringVar()
        
        # Main Frames
        self._main_menu_frame = tk.Frame(root)
        self._build_main_menu_ui()  
        self._main_menu_frame.pack(fill="both", expand=True)   # ← added options
        self._main_menu_frame.pack_propagate(False)            # ← keep full size
                
        self._setup_frame = tk.Frame(root)
        self._build_setup_ui()
        

        self._game_frame = tk.Frame(root)
        self._build_game_ui()
        
        # UI Elements

        self._skip_button = None 
        self.worker_icon = tk.PhotoImage(
            file=os.path.join(getattr(sys, "_MEIPASS", os.getcwd()), "assets", "worker.png")
        ).subsample(2, 2)
        

    def _build_main_menu_ui(self) -> None:
        """Build the main menu UI."""
        frame = self._main_menu_frame

        # Title Label
        title_lbl = tk.Label(frame,text="Santorini",font=("Arial", 48, "bold"),bg="white")
        title_lbl.place(relx=0.5, rely=0.25, anchor="center")
        
        # Button for starting a new game
        start_btn = tk.Button(frame, text="Start New Game",
                              font=("Arial",18), width=20,
                              command=self._show_setup_screen)
        start_btn.place(relx=0.5, rely=0.5, anchor="n")

        # Button for exiting the game
        exit_btn = tk.Button(frame, text="Exit",
                             font=("Arial",18), width=20,
                             command=self._root.destroy)
        exit_btn.place(relx=0.5, rely=0.6, anchor="n")
        
    def _build_setup_ui(self) -> None:
        """Build the setup UI."""
        frame = self._setup_frame
        frame.pack_propagate(False)

        win_w = self._root.winfo_width()
        win_h = self._root.winfo_height()
        canvas = tk.Canvas(frame, width=win_w, height=win_h, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Player 1 block
        canvas.create_text(win_w//2, win_h*0.20,
                        text="Player 1", font=("Arial",24,"bold"), fill="black")

        # “Name” label + entry
        e1 = tk.Entry(frame, font=("Arial",16), width=20, textvariable=self._player1_name_var)
        canvas.create_window(win_w//2, win_h*0.25, window=e1, width=300, height=30)

        # “Color” label + dropdown
        canvas.create_text(win_w//2, win_h*0.30,
                        text="Color:", font=("Arial",16,"bold"), fill="black")
        om1 = tk.OptionMenu(frame, self._player1_color_var, *[c.name for c in Color])
        om1.config(font=("Arial",14))
        canvas.create_window(win_w//2, win_h*0.33, window=om1, width=200, height=30)

        # Player 2 block
        canvas.create_text(win_w//2, win_h*0.40,
                        text="Player 2", font=("Arial",24,"bold"), fill="black")

        # “Name” label + entry
        e2 = tk.Entry(frame, font=("Arial",16), width=20, textvariable=self._player2_name_var)
        canvas.create_window(win_w//2, win_h*0.45, window=e2, width=300, height=30)

        # Color + dropdown
        canvas.create_text(win_w//2, win_h*0.50,
                text="Color:", font=("Arial",16,"bold"), fill="black")
        om2 = tk.OptionMenu(frame, self._player2_color_var, *[c.name for c in Color])
        om2.config(font=("Arial",14))
        canvas.create_window(win_w//2, win_h*0.53, window=om2, width=200, height=30)


        start_btn = tk.Button(frame, text="Start Game", font=("Arial",16),
                            width=12, command=self.start_game)

        canvas.create_window(win_w//2, win_h*0.70,
                            window=start_btn, anchor="center")
        
    def _show_setup_screen(self) -> None:
        """Show the setup screen."""
        self._main_menu_frame.pack_forget()  # Hide Main Menu
        self._setup_frame.pack(fill="both", expand=True)  # Show Setup Frame


    def _build_game_ui(self) -> None:
        """Build the game UI."""
        # Main container frame
        container_frame = tk.Frame(self._game_frame)
        container_frame.pack(fill="both", expand=True)
        
        # Top info panel for turn and phase (above the board)
        top_panel = tk.Frame(container_frame, bg="lightblue", height=40)
        top_panel.pack(fill="x", padx=10, pady=(10, 0))
        
        # Turn label on the left side of top panel
        self.turn_label = tk.Label(top_panel, text="Turn: ", font=("Arial", 12, "bold"), bg="lightblue")
        self.turn_label.pack(side="left", padx=20)
        
        # Phase label on the right side of top panel
        self.phase_label = tk.Label(top_panel, text="Phase: ", font=("Arial", 12, "bold"), bg="lightblue")
        self.phase_label.pack(side="right", padx=20)
        
        # God card name in the middle of top panel
        self.god_name = tk.Label(top_panel, text="God Card: ", font=("Arial", 12, "bold"), bg="lightblue")
        self.god_name.pack(side="top", pady=5)
        
        # Main content area (for board and sidebar)
        content_frame = tk.Frame(container_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Board container frame (centered)
        board_container = tk.Frame(content_frame)
        board_container.pack(side="left", fill="both", expand=True)
        
        # Create the board canvas inside a frame to center it
        board_frame = tk.Frame(board_container)
        board_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Canvas for the game board
        self.canvas = tk.Canvas(
            board_frame,
            width=self.BOARD_W * self.TILE,
            height=self.BOARD_H * self.TILE,
            bg="white"
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Sidebar on the right (gray background)
        sidebar = tk.Frame(content_frame, bg="gray", width=200)
        sidebar.pack(side="right", fill="y", padx=10)
        sidebar.pack_propagate(False)  # Keep the width fixed
        
        # Add the skip button in the middle of the sidebar
        sb_height = self._root.winfo_height() - 100  # Calculate height for sidebar
        filler_top = tk.Frame(sidebar, bg="gray", height=sb_height//2 - 20)
        filler_top.pack(fill="x")
        
        # Skip button
        self.skip_button = tk.Button(sidebar, text="Skip Action/Phase", command=self.on_skip, state="disabled",font=("Arial", 12),padx=10,pady=5)
        self.skip_button.pack(pady=20)
        
        # Bottom filler to keep button centered
        filler_bottom = tk.Frame(sidebar, bg="gray")
        filler_bottom.pack(fill="both", expand=True)
        
    def start_game(self) -> None:
        """Start the game with the selected player names and colors."""
        
        # Get player names and colors from the UI
        # Validate the inputs
        n1 = self._player1_name_var.get().strip()
        n2 = self._player2_name_var.get().strip()
        c1 = self._player1_color_var.get()
        c2 = self._player2_color_var.get()

        if not n1 or not n2:
            messagebox.showerror("Error", "Both players must enter their names.")
            return
        if not c1 or not c2:
            messagebox.showerror("Error", "Both players must select a color.")
            return
        if c1 == c2:
            messagebox.showerror("Error", "Players must choose different colors.")
            return
        
        # Create the players
        p1 = Player(n1, 0, Color[c1])
        p2 = Player(n2, 0, Color[c2])
        
        # Initialize the game instance with the players, board width, and height
        self._game = Game([p1, p2], self.BOARD_W, self.BOARD_H)
        
        self._setup_frame.pack_forget()
        self._game_frame.pack(fill="both", expand=True)
        self._game_frame.pack_propagate(False)
        self.draw_board()
    
    def draw_board(self) -> None:
        """Draw the game board and update the UI."""
        # Clear the canvas and reset the rectangle IDs
        self.canvas.delete("all")
        self._rect_ids.clear()

        # Get the selected worker position
        self._selected_worker_pos = self._game.selected_worker_pos()
        
        # Show the status of the game (turn, phase, god card)
        self.turn_label .config(text=f"Turn:  {self._game.current_player_name}")
        self.phase_label.config(text=f"Phase: {self._game.get_current_phase()}")
        self.god_name.config(text=f"God Card: {self._game.turn_manager.current_player.god_card.name}")
        
        # Draw the board
        # Draw the grid and tiles
        for x in range(self.BOARD_W):
            for y in range(self.BOARD_H):
                x0, y0 = x*self.TILE, y*self.TILE
                # Create a rectangle for each tile
                rect = self.canvas.create_rectangle(
                    x0, y0, x0+self.TILE, y0+self.TILE,
                    fill="lightgreen", outline="black"
                )
                self._rect_ids[(x, y)] = rect
                
                # Get the tile object from the game board for each position
                tile = self._game.board.get_tile(Position(x, y))

                # Check if the tile has a building
                if tile.building:
                    # get the building level
                    lvl = tile.building.level

                    # Draw building levels 1-3 as stacked blocks
                    max_size = self.TILE - 20
                    shrink_per_level = 10
                    for l in range(min(lvl, 3)):  # only up to level 3 blocks
                        size = max_size - (l * shrink_per_level)
                        offset = (self.TILE - size) // 2
                        self.canvas.create_rectangle(
                            x0 + offset, y0 + offset,
                            x0 + self.TILE - offset, y0 + self.TILE - offset,
                            outline="gray", width=2
                        )

                    # If there is a dome (level >= 4), draw small blue dome on top of the last block
                    if lvl >= 4:
                        dome_radius = self.TILE // 8  # smaller dome
                        center_x = x0 + self.TILE // 2
                        center_y = y0 + self.TILE // 2
                        self.canvas.create_oval(
                            center_x - dome_radius, center_y - dome_radius,
                            center_x + dome_radius, center_y + dome_radius,
                            fill="blue", outline="black"
                        )

                # Check if the tile has a worker
                if tile.has_worker():
                    player_color = None
                    # Iterate through players to find the one with the worker
                    for pl in self._game.players:
                        if tile.worker in pl.all_workers:
                            # Get the color of the player
                            player_color = pl.player_color.name.lower()
                            break
                        
                    # If a worker is found, draw it
                    if player_color:
                        circle_radius = self.TILE // 4
                        center_x = x0 + self.TILE // 2
                        center_y = y0 + self.TILE // 2
                        
                        # Draw a circle for the worker
                        # Use the player's color for the circle
                        self.canvas.create_oval(
                            center_x - circle_radius, center_y - circle_radius,
                            center_x + circle_radius, center_y + circle_radius,
                            fill=player_color, outline=""
                        )
                        # Draw the worker icon on top of the circle
                        self.canvas.create_image(
                            center_x, center_y,
                            image=self.worker_icon
                        )

        # Highlight the selected worker
        if self._selected_worker_pos:
            sx, sy = self._selected_worker_pos
            self.canvas.itemconfig(self._rect_ids[(sx,sy)], fill="yellow")

        # If the game is in a phase where the player can skip, enable the skip button
        if self._game.current_phase_optional():
            self.skip_button.config(state="normal")
        # If not, disable it
        else:
            self.skip_button.config(state="disabled")
        
    def on_click(self, evt) -> None:
        """Handle mouse click events on the game board."""
        # If game is not initialized, do nothing
        if not self._game:
            return

        # Get the clicked tile coordinates
        bx, by = evt.x // self.TILE, evt.y // self.TILE
        
        # Check if the clicked tile is within bounds
        # and Get the tile object from the game board
        self._game.click_cell(bx, by)

        # Get result of the last action
        result = self._game.turn_manager.get_game_result()
        
        # Redraw the board to reflect the current state
        self.draw_board()
        
        # Check if the game is over
        if result:
            # Determine if it's win or lose
            if result == self._game.turn_manager.current_player:
                # Current player wins
                messagebox.showinfo("Game Over", f"{result.player_name} wins by reaching level 3!")
                # Go back to main menu
                self._game_frame.pack_forget()
                self._main_menu_frame.pack(fill="both", expand=True)
            else:
                # Opponent wins
                messagebox.showinfo("Game Over", f"{result.player_name} wins!")
                # Go back to main menu
                self._game_frame.pack_forget()
                self._main_menu_frame.pack(fill="both", expand=True)
            
            self._game_frame.pack_forget()
            self._setup_frame.pack()
            return


    def on_skip(self) -> None:
        """Handle the skip button click."""
        # If the current phase is optional, skip the phase
        if self._game and self._game.current_phase_optional():
            self._game.skip_phase()
            # Update the game UI to reflect the skipped phase
            self.draw_board()



if __name__ == "__main__":
    root = tk.Tk()
    app = SantoriniApp(root)
    root.mainloop()