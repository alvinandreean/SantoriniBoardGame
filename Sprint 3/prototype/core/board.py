from core.tile import Tile
from core.position import Position

class Board:
    """ Represents a Santorini game board """
    
    def __init__(self, width: int, height: int) -> None:
        """ 
        Initializes a board (HashMap/Dict) with the given width and height.
        
        Each tile on the board is represented by a Tile object.
        
        """
        self._width = width
        self._height = height
        self._tiles: dict[tuple[int, int], Tile] = {
            (x, y): Tile(Position(x, y))
            for x in range(width)
            for y in range(height)
        }

    @property
    def height(self) -> int:
        """
        Returns the height of the board.

        Returns:
            int: The number of rows.
        """
        return self._height

    @property
    def width(self) -> int:
        """
        Returns the width of the board.

        Returns:
            int: The number of columns.
        """
        return self._width

    def in_bounds(self, pos: Position) -> bool:
        """
        Checks if a given position is within the bounds of the board.

        Args:
            pos (Position): The position to check.

        Returns:
            bool: True if the position is within bounds, False otherwise.
        """
        return (pos.x, pos.y) in self._tiles

    def get_tile(self, pos: Position) -> Tile | None:
        """
        Retrieves the tile at a given position.

        Args:
            pos (Position): The position of the tile.

        Returns:
            Tile | None: The Tile object at the specified position, or None if out-of-bounds.
        """
        return self._tiles.get((pos.x, pos.y))

    def get_all_empty_tiles(self) -> list[Tile]:
        """
        Retrieves all tiles that have no worker and no building.

        Returns:
            list[Tile]: A list of all empty Tile objects on the board.
        """
        return [
            tile for tile in self._tiles.values()
            if tile.worker is None and tile.building is None
        ]
