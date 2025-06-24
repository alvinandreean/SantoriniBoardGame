from typing import List, Optional

from tutorial.tutorial_step import TutorialStep
from core.player import Player
from core.board import Board
from core.tile import Tile
from core.worker import Worker


class SelectWorkerStep(TutorialStep):
    """
    Tutorial step that teaches player how to select workers.
    Only allows clicking on current player's workers.
    """
    
    def get_step_name(self) -> str:
        """Get the name of this tutorial step."""
        return "Select Worker"
    
    def get_instructions(self) -> str:
        """Get instruction text to display to the user."""
        return ("Step 1: Select Your Worker\n\n"
                "Click on one of your workers (blue pieces) to select it.\n"
                "You can see your workers are highlighted on the board.\n\n"
                "Workers are the pieces you'll use to move and build!")
    
    def is_valid_tile_click(self, tile: Tile, current_player: Player, current_worker: Optional[Worker], phase: str) -> bool:
        """Only allow clicking on current player's workers during Select Worker phase."""
        if phase == "Select Worker":
            # Only allow selecting player's own workers
            if tile.worker is None or tile.worker.color != current_player.player_color:
                return False
            return True
        else:
            # Allow all other actions
            return True
    
    def get_highlighted_tiles(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> List[Tile]:
        """Highlight tiles containing current player's workers only during Select Worker phase."""
        # Only highlight workers during "Select Worker" phase
        if phase != "Select Worker":
            return []
            
        highlighted_tiles = []
        
        for worker in current_player.workers:
            tile = board.get_tile(worker.position)
            highlighted_tiles.append(tile)
        
        return highlighted_tiles
    
    def is_step_complete(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> bool:
        """Step complete when worker is selected."""
        return current_worker is not None
    
    def should_auto_advance(self) -> bool:
        """Auto advance when worker is selected."""
        return True 