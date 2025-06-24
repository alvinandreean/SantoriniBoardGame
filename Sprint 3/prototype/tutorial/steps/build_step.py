from typing import List, Optional

from tutorial.tutorial_step import TutorialStep
from core.player import Player
from core.board import Board
from core.tile import Tile
from core.worker import Worker
from utils.validator import Validator


class BuildStep(TutorialStep):
    """
    Tutorial step that teaches player how to build.
    Only allows valid build tiles as determined by the game validator.
    """
    
    def get_step_name(self) -> str:
        """Get the name of this tutorial step."""
        return "Build Structure"
    
    def get_instructions(self) -> str:
        """Get instruction text to display to the user."""
        return ("Step 3: Build a Structure\n\n"
                "Click on a highlighted tile adjacent to your worker to build.\n"
                "Buildings have 4 levels: 1, 2, 3, and Dome.\n\n"
                "Rules:\n"
                "• Must build adjacent to your worker\n"
                "• Can't build on occupied tiles\n"
                "• Can't build on domed tiles\n"
                "• Domes complete the building")
    
    def is_valid_tile_click(self, tile: Tile, current_player: Player, current_worker: Optional[Worker], phase: str) -> bool:
        """Allow all clicks - let normal game validation handle it."""
        # Allow all tile clicks for build step - normal game validation will handle restrictions
        return True
    
    def get_highlighted_tiles(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> List[Tile]:
        """Highlight valid build tiles."""
        if current_worker is None or phase != "Build":
            return []
        
        # Get valid build tiles from validator
        valid_tiles = Validator.get_valid_build_tiles(current_worker, board)
        return valid_tiles if valid_tiles else []
    
    def is_step_complete(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> bool:
        """Step complete when build phase is done."""
        return phase == "End Turn"
    
    def should_auto_advance(self) -> bool:
        """Auto advance when build is complete."""
        return True 