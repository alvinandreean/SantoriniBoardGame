from typing import List
import random

from player import Player
from worker import Worker
from board import Board
from turn_manager import TurnManager
from god_cards.god_card_deck import GodCardDeck
from position import Position


class Game:
    """Represents a Santorini game instance."""
    
    def __init__(self, players: List[Player], width: int = 5, height: int = 5) -> None:
        """Initializes a game with the given players and board dimensions."""
        self._board = Board(width, height)
        self._players = players            
        self._god_deck = GodCardDeck()
        
        # For each player, place two workers randomly on the board 
        # and draw a god card.
        for p in self._players:
            self._place_random_workers(p)
            self._pick_random_god(p)
        
        # Initialize the turn manager with the players and board.     
        self.turn_manager = TurnManager(self._players, self._board)
        
    @property
    def board(self) -> Board:
        """Returns the game board."""
        return self._board
    
    @property
    def players(self) -> List[Player]:
        """Returns the players in the game."""
        return self._players
    
    @property
    def current_player_name(self) -> str:
        """Returns the name of the current player."""
        return self.turn_manager.current_player.player_name
    
    
    def get_current_phase(self) -> str:
        """
        Returns the current phase of the game.
        
        - "Select Worker" (haven’t picked yet)
        - "Move" (next step is a MoveAction)
        - "Build" (next step is a BuildAction)
        - "End Turn" (no more steps)
        
        """
        return self.turn_manager.get_phase()
    
    def current_phase_optional(self) -> bool:
        """Returns True if the current phase is optional."""
        return self.turn_manager.current_phase_optional()
    
    def skip_phase(self) -> None:
        """Skip the current phase. Only valid if the phase is optional."""
        return self.turn_manager.skip_phase()
    
    def _place_random_workers(self, player: Player) -> None:
        """Places two workers randomly on the board."""
        # Get all empty tiles on the board and shuffle them.
        tiles = self._board.get_all_empty_tiles()
        random.shuffle(tiles)
        
        # Place two workers on the first two shuffled tiles.
        for tile in tiles[:2]:
            w = Worker(tile.position, player.player_color)
            # Assign the worker to the tile and add it to the player.
            player.add_worker(w)
            tile.worker = w

    def _pick_random_god(self, player: Player) -> None:
        """Picks a random god card for the player."""
        player._player_god = self._god_deck.draw()
        
    def selected_worker_pos(self) -> tuple[int,int] | None:
        """Returns the position of the currently selected worker."""
        # if no worker is selected, return None
        w = self.turn_manager.worker
        if not w:
            return None
        
        # if a worker is selected, return its position
        p = w.position
        return p.x, p.y
    
    def click_cell(self, bx: int, by: int) -> bool:
        """Handles a click on the board."""
        
        # Check for out-of-bounds clicks.
        if not (0 <= bx < self._board.width and 0 <= by < self._board.height):
            return

        # Get the tile at the clicked position and handle the click.
        tile = self._board.get_tile(Position(bx, by))
        return self.turn_manager.handle_click(tile)