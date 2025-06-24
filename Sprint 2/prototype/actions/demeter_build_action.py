from actions.build_action import BuildAction
from tile import Tile
from worker import Worker
from board import Board


class DemeterBuildAction(BuildAction):
    """Represents the action of building on a tile with Demeter's special ability."""
    def validate(self, worker: Worker, board: Board, tile: Tile) -> bool:
        """Override the validate method to include Demeter's special ability constraint."""
        
        # Can't build on the tile where the worker previously built
        forbidden = worker.previous_build_pos
        if tile.position == forbidden:
            return False
        
        # The rest of the validation is the same as the base class
        return super().validate(worker, board, tile)