from core.position import Position
from buildings.building import Building
from core.worker import Worker


class Tile:
    """Represents a single tile on the Santorini game board."""
    
    def __init__(self, position: Position | None) -> None:
        """ 
        Initialize a tile at *position*.
        
        A tile may later hold a worker and/or a building.
        
        """
        self._position: Position = position
        self._worker = None
        self._building = None
    
    @property
    def position(self) -> Position:
        """Returns the position of the tile."""
        return self._position
    
    @property
    def building(self) -> Building | None:
        """Returns the building on the tile."""
        return self._building
    
    @building.setter
    def building(self, building) -> None:
        """Sets a building on the tile."""
        self._building = building
    
    @property 
    def worker(self) -> Worker | None:
        """Returns the worker on the tile. """
        return self._worker
    
    @worker.setter
    def worker(self, worker) -> None:
        """Places a worker on the tile."""
        self._worker = worker
    
    def has_worker(self) -> bool:
        """ 
        Checks if the tile has a worker.
        
        Returns True if the tile has a worker, False otherwise.
        
        """
        return self._worker is not None
    
    