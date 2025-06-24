from typing import List, Optional

from tutorial.tutorial_step import TutorialStep
from core.player import Player
from core.board import Board
from core.tile import Tile
from core.worker import Worker


class CompletionStep(TutorialStep):
    """
    Final tutorial step that congratulates the player.
    This step marks the end of the tutorial.
    """
    
    def __init__(self, tutorial_type: str = "basic") -> None:
        """Initialize completion step with tutorial type."""
        self._tutorial_type = tutorial_type
    
    def get_step_name(self) -> str:
        """Get the name of this tutorial step."""
        return "Tutorial Complete"
    
    def get_instructions(self) -> str:
        """Get instruction text to display to the user."""
        if self._tutorial_type == "basic":
            return ("Congratulations! \n\n"
                    "You've completed the Basic Tutorial!\n\n"
                    "You now know how to:\n"
                    "• Select and move workers\n"
                    "• Build structures properly\n"
                    "• Follow the game sequence: Move -> Build\n\n"
                    "Try the Win and Lose tutorials next to master\n"
                    "all aspects of Santorini!\n\n"
                    "Click the Main Menu button to return to the main menu.")
        
        elif self._tutorial_type == "win":
            return ("Congratulations! \n\n"
                    "You've completed the Win Tutorial!\n\n"
                    "You now understand:\n"
                    "• How to build up to level 3\n"
                    "• How to position for victory\n"
                    "• The winning condition: Move to level 3\n\n"
                    "You're ready to claim victory in real games!\n\n"
                    "Click the Main Menu button to return to the main menu.")
        
        else:  # lose
            return ("Congratulations! \n\n"
                    "You've completed the Lose Tutorial!\n\n"
                    "As you can see, the worker cannot move anywhere:\n"
                    "• Cannot climb from level 0 to level 2\n"
                    "• Cannot move to domed tiles\n"
                    "• Your other worker is also blocked\n\n"
                    "You now understand:\n"
                    "• How workers can get trapped by height\n"
                    "• When you lose the game (no valid moves)\n"
                    "• The importance of strategic positioning\n\n"
                    "This knowledge will help you avoid defeat\n"
                    "and play more strategically!\n\n"
                    "Click the Main Menu button to return to the main menu.")
    
    def is_valid_tile_click(self, tile: Tile, current_player: Player, current_worker: Optional[Worker], phase: str) -> bool:
        """Block all tile clicks except exit button during completion."""
        return False  # Block all tile interactions during completion
    
    def get_highlighted_tiles(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> List[Tile]:
        """No tiles highlighted during completion."""
        return []
    
    def is_step_complete(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> bool:
        """Completion step is immediately complete."""
        return True
    
    def should_auto_advance(self) -> bool:
        """Don't auto advance - wait for user to click."""
        return False 