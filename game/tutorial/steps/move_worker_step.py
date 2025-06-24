from typing import List, Optional

from tutorial.tutorial_step import TutorialStep
from core.player import Player
from core.board import Board
from core.tile import Tile
from core.worker import Worker
from utils.validator import Validator


class MoveWorkerStep(TutorialStep):
    """
    Tutorial step that teaches player how to move workers.
    Only allows valid moves as determined by the game validator.
    """
    
    def get_step_name(self) -> str:
        """Get the name of this tutorial step."""
        return "Move Worker"
    
    def get_instructions(self) -> str:
        """Get instruction text to display to the user."""
        return ("Step 2: Move Your Worker\n\n"
                "Click on a highlighted tile to move your selected worker.\n"
                "You can move to adjacent tiles (including diagonally).\n\n"
                "Rules:\n"
                "• Can't move to occupied tiles\n"
                "• Can't move up more than 1 level\n"
                "• Can't move to domed tiles")
    
    def is_valid_tile_click(self, tile: Tile, current_player: Player, current_worker: Optional[Worker], phase: str) -> bool:
        """Allow all clicks - let normal game validation handle it."""
        # Allow all tile clicks for move step - normal game validation will handle restrictions
        return True
    
    def get_highlighted_tiles(self, current_player: Player,
                             current_worker: Optional[Worker],
                             phase: str, board: Board) -> List[Tile]:
        """Highlight valid move tiles when a worker is selected."""
        # Show move highlights if we have a selected worker
        if current_worker is None:
            return []
        
        # Get valid move tiles from validator
        valid_tiles = Validator.get_valid_move_tiles(current_worker, board)
        return valid_tiles if valid_tiles else []
    
    def is_step_complete(self, current_player: Player,
                        current_worker: Optional[Worker],
                        phase: str, board: Board) -> bool:
        """Step complete when move phase is done and we advance to build."""
        return phase == "Build"
    
    def should_auto_advance(self) -> bool:
        """Auto advance when move is complete."""
        return True 