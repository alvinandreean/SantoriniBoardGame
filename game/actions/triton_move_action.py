from actions.move_action import MoveAction
from actions.action_result import ActionResult
from core.worker import Worker
from core.board import Board
from core.tile import Tile
from core.position import Position



class TritonMoveAction(MoveAction):
    """Represents the action of moving a worker to a new tile with Triton's special ability."""
    
    def __init__(self, optional: bool = False):
        """Initialize the Triton move action as optional"""
        super().__init__(optional)
    
    def execute(self, worker: Worker, board: Board, tile: Tile) -> ActionResult:
        """Execute the move and check if we should add another optional move."""
        # First, perform the standard move using parent class
        super().execute(worker, board, tile)
        
        # Then check if destination is perimeter space for chaining
        if self._is_perimeter_space(tile.position, board):
            # Add another optional TritonMoveAction for chaining
            next_move = TritonMoveAction(optional=True)
            return ActionResult([next_move])
        else:
            # Normal move completion - no chaining
            return ActionResult()
    
    def _is_perimeter_space(self, position: Position, board: Board) -> bool:
        """Check if the position is on the perimeter of the board."""
        return (position.x == 0 or 
                position.x == board.width - 1 or 
                position.y == 0 or 
                position.y == board.height - 1) 