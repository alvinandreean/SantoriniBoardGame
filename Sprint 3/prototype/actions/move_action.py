from actions.action   import Action
from core.worker   import Worker
from core.board    import Board
from utils.validator import Validator
from core.tile import Tile
from actions.action_result import ActionResult

class MoveAction(Action):
    """Represents the action of moving a worker to a new tile."""
    def execute(self, worker: Worker, board: Board, tile: Tile) -> ActionResult:
        """Execute the move action on the given tile."""
        new_tile = tile
        if new_tile.worker is not None: # Check if the target tile already has a worker
            raise ValueError("MoveAction: target tile already has a worker")

        # 1) Remove the worker from its old tile
        old_tile = board.get_tile(worker.position)
        old_tile.worker = None

        # 2) Move the worker to the new tile
        new_tile.worker = worker

        # 3) Update the worker's position
        worker.position = tile.position
        
        # Standard move - no additional actions
        return ActionResult()

    def validate(self, worker: Worker, board: Board, tile: Tile) -> bool:
        """Validate the move action."""
        return tile in Validator.get_valid_move_tiles(worker, board)