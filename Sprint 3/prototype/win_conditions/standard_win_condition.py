from core.player import Player
from core.worker import Worker
from core.board import Board
from utils.validator import Validator
from win_conditions.win_condition_strategy import WinConditionStrategy


class StandardWinCondition(WinConditionStrategy):
    """Standard Santorini win condition: move to level 3."""
    
    def check_win(self, player: Player, worker: Worker, board: Board) -> bool:
        """
        Check if player wins by moving to level 3.
        Win condition: Worker moves from level 2 to level 3.
        """
        if not worker:
            return False
            
        # Get current tile and building level
        current_tile = board.get_tile(worker.position)
        building = current_tile.building
        
        # Must be on level 3 to potentially win
        if not building or building.level != 3:
            return False
            
        # Check previous position and level
        prev_pos = worker.previous_position
        if not prev_pos:
            return False
            
        prev_tile = board.get_tile(prev_pos)
        prev_level = (prev_tile.building.level 
                     if prev_tile and prev_tile.building 
                     else 0)
        
        # Win if moved from level 2 to level 3
        return prev_level == 2
    
    def check_lose(self, player: Player, board: Board) -> bool:
        """
        Check if player loses by having no valid moves.
        Lose condition: All workers unable to move.
        """
        # Check if any worker can move
        for worker in player.all_workers:
            valid_moves = Validator.get_valid_move_tiles(worker, board)
            if valid_moves:
                return False  # At least one worker can move
                
        return True  # No workers can move 