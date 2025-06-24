from typing import List, Optional

from tutorial.tutorial_step import TutorialStep
from core.player import Player
from core.board import Board
from core.tile import Tile
from core.worker import Worker
from core.position import Position


class MoveToTrapStep(TutorialStep):
    """
    Lose tutorial step that teaches about losing by getting trapped.
    Forces player to make a move that results in all workers being blocked.
    """
    
    def __init__(self) -> None:
        """Initialize the move to trap step."""
        self._move_completed = False
        self._demonstration_shown = False
        self._step_completed = False
    
    def get_step_name(self) -> str:
        """Get the name of this tutorial step."""
        return "Experience the Lose Condition"
    
    def get_instructions(self) -> str:
        """Get instruction text to display to the user."""
        if not self._move_completed:
            return ("Lose Tutorial: Height Trap! \n\n"
                    "Learn how building heights can trap you.\n\n"
                    "Current situation:\n"
                    "• Blue worker at (1,1) on level 2 building\n"
                    "• Blue worker at (4,4) already blocked by opponents\n"
                    "• Domes at (1,0) and (0,1) block movement\n"
                    "Task: For tutorial purposes, we will move\n"
                    "the worker from (1,1) to (0,0)\n"
                    "This creates a height trap - you can't climb\n"
                    "back up from level 0 to level 2!\n\n"
                    "Learn: Height differences matter in Santorini!")

    def is_valid_tile_click(self, tile: Tile, current_player: Player, current_worker: Optional[Worker], phase: str) -> bool:
        """Force select only the free worker and restrict moves to highlighted tiles only."""
        # Block all actions if step is already completed
        if self._step_completed:
            return False
        
        if phase == "Select Worker":
            # Only allow selecting the worker at (1,1) 
            if tile.worker is None or tile.worker.color != current_player.player_color:
                return False
            
            worker_pos = tile.worker.position
            is_correct_position = worker_pos.x == 1 and worker_pos.y == 1
            
            return is_correct_position
            
        elif phase == "Move":
            # Only allow moves to the highlighted trap tile (0,0)
            if current_worker is None:
                return False
                
            # Check if clicking on the trap position (0,0)
            return tile.position.x == 0 and tile.position.y == 0
            
        else:
            # For other phases (like Build), allow normal game validation
            return True
    
    def get_highlighted_tiles(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> List[Tile]:
        """Highlight appropriate tiles based on the tutorial phase."""
        if not self._move_completed:
            if phase == "Select Worker":
                # Only highlight the specific worker at (1,1)
                target_tile = board.get_tile(Position(1, 1))
                
                # Check if there's a player worker there
                if (target_tile.worker is not None and 
                    target_tile.worker.color == current_player.player_color):
                    return [target_tile]
                return []
            
            elif phase == "Move" and current_worker is not None:
                # Only highlight the trap position at (0,0) if it's reachable
                target_tile = board.get_tile(Position(0, 0))
                
                # Check if worker can reach it
                worker_pos = current_worker.position
                dx = abs(worker_pos.x - 0) 
                dy = abs(worker_pos.y - 0)  
                is_adjacent = dx <= 1 and dy <= 1 and (dx != 0 or dy != 0)
                
                # Check if tile is not occupied by player worker
                not_occupied_by_player = target_tile.worker is None or target_tile.worker.color != current_player.player_color
                
                if is_adjacent and not_occupied_by_player:
                    return [target_tile]
        else:
            # After move completed - highlight the trapped worker for demonstration
            if phase == "Select Worker":
                target_tile = board.get_tile(Position(0, 0))
                
                # Check if there's a player worker there (the trapped one)
                if (target_tile.worker is not None and 
                    target_tile.worker.color == current_player.player_color):
                    return [target_tile]
        
        return []
    
    def is_step_complete(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> bool:
        """Step complete immediately after moving to trap."""
        # Check if the worker has moved to the trap position (0,0)
        trap_tile = board.get_tile(Position(0, 0))
        worker_at_trap = (trap_tile.worker is not None and 
                        trap_tile.worker.color == current_player.player_color)
        
        # Complete immediately when worker reaches trap
        if worker_at_trap:
            self._step_completed = True
            return True
        return False
    
    def handle_tile_click(self, tile: Tile, current_player: Player, current_worker: Optional[Worker], phase: str) -> None:
        """Handle tile clicks to progress the demonstration."""
        if self._move_completed and phase == "Select Worker":
            # Check if user clicked on the trapped worker
            if (tile.worker is not None and 
                tile.worker.color == current_player.player_color and
                tile.worker.position.x == 0 and tile.worker.position.y == 0):
                self._demonstration_shown = True
    
    def should_auto_advance(self) -> bool:
        """Don't auto advance - require user interaction to complete the demonstration."""
        return True