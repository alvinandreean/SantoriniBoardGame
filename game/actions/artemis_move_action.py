from actions.move_action import MoveAction
from core.tile import Tile
from core.worker import Worker
from core.board import Board


class ArtemisMoveAction(MoveAction):
    """Represents the action of moving a worker to a new tile with Artemis's special ability."""
    def validate(self, worker: Worker, board: Board, tile: Tile) -> bool:
        """Override the validate method to include Artemis's special ability constraint."""
        
        # Can't move to the tile where the worker previously moved
        forbidden = worker.previous_position
        if tile.position == forbidden:
            return False
        
        # The rest of the validation is the same as the base class
        return super().validate(worker, board, tile)