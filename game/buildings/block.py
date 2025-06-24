from buildings.building import Building
from buildings.dome import Dome



class Block(Building):
    """A Block is a building that can be at level 1, 2, or 3."""

    def __init__(self, level: int = 1) -> None:
        """ 
        Initialise a Block at level 1, 2, or 3.
        
        If level is not in this range, raise ValueError.
        """
        if not (1 <= level <= 3):
            raise ValueError("Block level must be 1–3")
        self._level = level

    def has_dome(self) -> bool:
        """Returns False, as a Block cannot have a dome."""
        return False

    @property
    def level(self) -> int:
        """Returns the level of the Block."""
        return self._level

    def increase_level(self) -> Building:
        """Increase the level of the Block by one."""
        if self._level < 3: # Block can be increased to level 3 at most
            return Block(self._level + 1)
        
        # If the Block is already at level 3, it becomes a Dome
        return Dome()
