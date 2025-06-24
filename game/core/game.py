from typing import List
import random

from core.player import Player
from core.board import Board
from game_management.turn_manager import TurnManager
from god_cards.god_card_deck import GodCardDeck
from core.position import Position
from core.tile import Tile
from god_cards.god_card_factory import GodCardFactory
from game_management.game_input_handler import GameInputHandler
from game_modes.game_mode import GameMode
from game_modes.standard_game_mode import StandardGameMode
from win_conditions.win_condition_strategy import WinConditionStrategy
from win_conditions.win_condition_checker import StandardWinCondition
from win_conditions.timer_win_condition import TimerWinCondition
from win_conditions.composite_win_condition import CompositeWinCondition
from utils.timer_manager import TimerManager

from typing import Optional

class Game:
    """Represents a Santorini game instance."""
    
    def __init__(self, players: List[Player], width: int = 5, height: int = 5, game_mode: Optional[GameMode] = None, win_condition: Optional[WinConditionStrategy] = None) -> None:
        """Initializes a game with the given players and board dimensions."""
        self._board = Board(width, height)
        self._players = players            
        
        self._timer_manager = TimerManager(self._players)
        # Set up game mode (default to standard mode)
        self._game_mode = game_mode if game_mode else StandardGameMode()
        
        if win_condition:
            self._win_condition = win_condition
        else:
            standard_condition = StandardWinCondition()
            timer_condition = TimerWinCondition()
            composite_condition = CompositeWinCondition([standard_condition, timer_condition])
            self._win_condition = composite_condition
        
        self._game_mode.initialize_game(self._players, self._board)
        
        if not self._is_tutorial_mode():
            available_cards = GodCardFactory.get_available_card_names()
            self._god_deck = GodCardDeck(available_cards)
            for p in self._players:
                self._pick_random_god(p)
        else:
            from god_cards.standard_god_card import StandardGodCard
            for p in self._players:
                p._player_god = StandardGodCard()
            
        # Initialize the turn manager with the players and board.     
        self.turn_manager = TurnManager(self._players, self._board, self._timer_manager, self._win_condition)
        self._input_handler = GameInputHandler(self.turn_manager)
    
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
    
    @property
    def game_mode(self) -> GameMode:
        """Returns the current game mode."""
        return self._game_mode
    
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
        """Handles a click on the board and returns feedback message."""
        
        # Check for out-of-bounds clicks.
        if not (0 <= bx < self._board.width and 0 <= by < self._board.height):
            return

        # Get the tile at the clicked position and handle the click.
        tile = self._board.get_tile(Position(bx, by))
        
        # Check with game mode if this click is valid
        current_player = self.turn_manager.current_player
        current_worker = self.turn_manager.worker
        current_phase = self.get_current_phase()
        
        if not self._game_mode.is_valid_tile_click(tile, current_player, current_worker, current_phase):
            return "Invalid move for current tutorial step."
        
        # Handle the click with input handler
        result = self._input_handler.handle_tile_click(tile)
        
        # Notify game mode of tile click using polymorphism (works for all modes)
        self._game_mode.handle_tile_click(current_player, current_worker, current_phase, self._board)
        
        return result
    
    def get_current_player_timer_info(self) -> Optional[dict]:
        """Get timer information for the current player."""
        return self._timer_manager.get_current_player_timer_info()
    
    def get_all_players_timer_info(self) -> dict:
        """Get timer information for all players."""
        return self._timer_manager.get_all_players_timer_info()
    
    def should_end_game(self) -> bool:
        """Check if game should end according to game mode."""
        return self._game_mode.should_end_game()
    
    def get_guidance_message(self) -> Optional[str]:
        """Get guidance message from game mode (for tutorial)."""
        current_player = self.turn_manager.current_player
        current_worker = self.turn_manager.worker
        current_phase = self.get_current_phase()
        
        return self._game_mode.get_guidance_message(current_player, current_worker, current_phase)
    
    def get_highlighted_tiles(self) -> List['Tile']:
        """Get tiles to highlight from game mode (for tutorial)."""
        current_player = self.turn_manager.current_player
        current_worker = self.turn_manager.worker
        current_phase = self.get_current_phase()
        
        return self._game_mode.get_highlighted_tiles(current_player, current_worker, current_phase, self._board)
    
    def _is_tutorial_mode(self) -> bool:
        """Check if current game mode is tutorial."""
        return self._game_mode.get_mode_name() == "Tutorial"