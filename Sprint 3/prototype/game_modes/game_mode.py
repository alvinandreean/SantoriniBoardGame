from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.player import Player
    from core.board import Board
    from core.tile import Tile
    from core.worker import Worker


class GameMode(ABC):
    """
    Strategy interface for different game modes.
    Follows Strategy Pattern to allow switching between tutorial and standard modes.
    """
    
    @abstractmethod
    def initialize_game(self, players: List['Player'], board: 'Board') -> None:
        """Initialize the game mode with players and board."""
        pass
    
    @abstractmethod
    def is_valid_tile_click(self, tile: 'Tile', current_player: 'Player', 
                           current_worker: Optional['Worker'], phase: str) -> bool:
        """Check if a tile click is valid in this game mode."""
        pass
    
    @abstractmethod
    def get_guidance_message(self, current_player: 'Player', 
                            current_worker: Optional['Worker'], phase: str) -> Optional[str]:
        """Get guidance message for current state (None for standard mode)."""
        pass
    
    @abstractmethod
    def get_highlighted_tiles(self, current_player: 'Player', 
                             current_worker: Optional['Worker'], 
                             phase: str, board: 'Board') -> List['Tile']:
        """Get list of tiles to highlight for current phase."""
        pass
    
    @abstractmethod
    def should_end_game(self) -> bool:
        """Check if the game should end (tutorial completion, etc.)."""
        pass
    
    @abstractmethod
    def get_mode_name(self) -> str:
        """Get the name of this game mode."""
        pass
    
    @abstractmethod
    def handle_post_action_update(self, current_player: 'Player', 
                                 current_worker: Optional['Worker'], 
                                 phase: str, board: 'Board') -> None:
        """Handle updates after an action has been processed."""
        pass
    
    def handle_tile_click(self, current_player: 'Player', 
                         current_worker: Optional['Worker'], 
                         phase: str, board: 'Board') -> None:
        """Handle tile click for mode-specific logic (e.g. tutorial progression).
        
        Default implementation does nothing (for standard mode).
        Tutorial mode overrides this for step progression.
        """
        pass 