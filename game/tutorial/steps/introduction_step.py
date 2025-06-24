from typing import List, Optional

from tutorial.tutorial_step import TutorialStep
from core.player import Player
from core.board import Board
from core.tile import Tile
from core.worker import Worker


class IntroductionStep(TutorialStep):
    """
    First tutorial step that introduces the game and tutorial.
    Waits for any click to continue.
    """
    
    def __init__(self, tutorial_type: str = "basic") -> None:
        """Initialize introduction step with tutorial type."""
        self._tutorial_type = tutorial_type
    
    def get_step_name(self) -> str:
        """Get the name of this tutorial step."""
        return "Introduction"
    
    def get_instructions(self) -> str:
        """Get instruction text to display to the user."""
        if self._tutorial_type == "basic":
            return ("Welcome to the Santorini Tutorial! 🏛️\n\n"
                    "This tutorial will teach you the fundamentals:\n"
                    "• How to select workers\n"
                    "• How to move around the board\n"
                    "• How to build structures\n"
                    "• The game sequence: Move → Build\n\n"
                    "Click anywhere to begin!")
        elif self._tutorial_type == "win":
            return ("Welcome to the Win Tutorial! 🏆\n\n"
                    "Learn how to achieve victory in Santorini:\n"
                    "• Build structures up to level 3\n"
                    "• Position your workers strategically\n"
                    "• Move to level 3 to win!\n\n"
                    "Click anywhere to begin!")
        else:  # lose
            return ("Welcome to the Lose Tutorial! 📚\n\n"
                    "Learn how to avoid defeat in Santorini:\n"
                    "• Understand when workers get trapped\n"
                    "• See what happens when you can't move\n"
                    "• Learn strategic positioning\n\n"
                    "Click anywhere to begin!")
    
    def is_valid_tile_click(self, tile: Tile, current_player: Player, current_worker: Optional[Worker], phase: str) -> bool:
        """Any tile click advances from introduction."""
        return True
    
    def get_highlighted_tiles(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> List[Tile]:
        """No tiles highlighted during introduction."""
        return []
    
    def is_step_complete(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> bool:
        """Introduction completes immediately after first display."""
        return False  # Will be marked complete after first tile click
    
    def should_auto_advance(self) -> bool:
        """Introduction should auto-advance after completion."""
        return True
    
    def handles_click_progression(self) -> bool:
        """Introduction step handles its own click progression."""
        return True 