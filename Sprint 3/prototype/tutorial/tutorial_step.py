from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.player import Player
    from core.board import Board
    from core.tile import Tile
    from core.worker import Worker


class TutorialStep(ABC):
    """
    State interface for individual tutorial steps.
    Each step knows what actions are valid and provides guidance.
    """
    
    @abstractmethod
    def get_step_name(self) -> str:
        """Get the name of this tutorial step."""
        pass
    
    @abstractmethod
    def get_instructions(self) -> str:
        """Get instruction text to display to the user."""
        pass
    
    @abstractmethod
    def is_valid_tile_click(self, tile: 'Tile', current_player: 'Player', current_worker: Optional['Worker'], phase: str) -> bool:
        """Check if a tile click is valid for this tutorial step."""
        pass
    
    @abstractmethod
    def get_highlighted_tiles(self, current_player: 'Player', current_worker: Optional['Worker'], phase: str, board: 'Board') -> List['Tile']:
        """Get tiles to highlight for this step."""
        pass
    
    @abstractmethod
    def is_step_complete(self, current_player: 'Player', current_worker: Optional['Worker'], phase: str, board: 'Board') -> bool:
        """Check if this tutorial step is complete."""
        pass
    
    @abstractmethod
    def should_auto_advance(self) -> bool:
        """Check if this step should automatically advance when complete."""
        pass
    
    def handles_click_progression(self) -> bool:
        """Check if this step handles its own click progression logic."""
        return False
    
    def handle_tile_click(self, tile: 'Tile', current_player: 'Player', current_worker: Optional['Worker'], phase: str) -> None:
        """Handle tile clicks for custom tutorial step logic."""
        pass 