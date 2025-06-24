from typing import List, Optional

from tutorial.tutorial_step import TutorialStep
from core.player import Player
from core.board import Board
from core.tile import Tile
from core.worker import Worker
from core.position import Position


class MoveToLevel3Step(TutorialStep):
    """Win tutorial step that teaches moving to level 3 to win."""
    
    def __init__(self) -> None:
        """Initialize the move to level 3 step."""
        self._step_completed = False
    
    def get_step_name(self) -> str:
        """Get the name of this tutorial step."""
        return "Move to Level 3 to Win"
    
    def get_instructions(self) -> str:
        """Get instruction text to display to the user."""
        return ("Win Tutorial: Move to Level 3! \n\n"
                "Your goal is to achieve victory in Santorini.\n\n"
                "Steps to win:\n"
                "1. Select the blue worker on level 2 at (2,2)\n"
                "2. Move to the level 3 building at (3,3)\n"
                "3. Achieve victory!\n\n"
                "Note: You can only climb 1 level at a time.\n"
                "Only the correct worker and winning move are allowed!")
    
    def is_valid_tile_click(self, tile: Tile, current_player: Player, current_worker: Optional[Worker], phase: str) -> bool:
        """Force select only the level 2 worker and block all actions after winning move."""
        # Block all actions if step is already completed
        if self._step_completed:
            return False
        
        if phase == "Select Worker":
            # Only allow selecting the worker at (2,2) on level 2
            if tile.worker is None or tile.worker.color != current_player.player_color:
                return False
            
            worker_pos = tile.worker.position
            is_correct_position = worker_pos.x == 2 and worker_pos.y == 2
            is_on_level_2 = tile.building is not None and tile.building.level == 2
            
            return is_correct_position and is_on_level_2
            
        elif phase == "Move":
            # Only allow moves to the highlighted level 3 tile (3,3)
            if current_worker is None:
                return False
                
            # Check if clicking on the level 3 position (3,3)
            return tile.position.x == 3 and tile.position.y == 3
            
        else:
            # Allow all other actions (builds) unless step is complete
            return True
    
    def get_highlighted_tiles(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> List[Tile]:
        """Highlight only the specific worker to select or only the level 3 building to move to."""
        if phase == "Select Worker":
            # Only highlight the specific worker on level 2 at position (2,2)
            target_tile = board.get_tile(Position(2, 2))
            
            # Check if there's a worker there and it's on level 2
            if (target_tile.worker is not None and 
                target_tile.worker.color == current_player.player_color and
                target_tile.building is not None and 
                target_tile.building.level == 2):
                return [target_tile]
            return []
        
        elif phase == "Move" and current_worker is not None:
            # Only highlight the level 3 building at (3,3) if it's reachable
            target_tile = board.get_tile(Position(3, 3))
            
            # Check if worker can reach it
            worker_pos = current_worker.position
            dx = abs(worker_pos.x - 3)  
            dy = abs(worker_pos.y - 3)  
            is_adjacent = dx <= 1 and dy <= 1 and (dx != 0 or dy != 0)
            
            is_level_3 = target_tile.building is not None and target_tile.building.level == 3
            not_occupied = target_tile.worker is None
            
            if is_adjacent and is_level_3 and not_occupied:
                return [target_tile]
        
        return []
    
    def is_step_complete(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> bool:
        """Step complete immediately when worker reaches level 3."""
        # Check if any of the player's workers is on level 3 - immediate win
        for x in range(board.width):
            for y in range(board.height):
                tile = board.get_tile(Position(x, y))
                if (tile.worker is not None and 
                    tile.worker.color == current_player.player_color and
                    tile.building is not None and 
                    tile.building.level == 3):
                    self._step_completed = True
                    return True
        return False
    
    def should_auto_advance(self) -> bool:
        """Auto advance when win condition is achieved."""
        return True 