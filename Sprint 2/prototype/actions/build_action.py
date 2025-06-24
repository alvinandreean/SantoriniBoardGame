from actions.action import Action
from worker import Worker
from board  import Board
from buildings.block  import Block
from validator import Validator
from tile import Tile

class BuildAction(Action):
    """Represents the action of building on a tile."""
    def execute(self, worker: Worker, board: Board, tile: Tile):
        """Execute the build action on the given tile."""

        # Check if the tile is empty and has no building
        if tile.building is None:
            # If the tile is empty, place a new building on it (level 1)
            tile.building = Block(1)
            
        # If the tile has a building, increase its level
        else: 
            new_building = tile.building.increase_level()
            tile.building = new_building

        # Update the previous build position of the worker
        worker.previous_build_pos = tile.position

        
    def validate(self, worker: Worker, board: Board, tile: Tile) -> bool:
        """Validate the build action."""
        return tile in Validator.get_valid_build_tiles(worker, board)
