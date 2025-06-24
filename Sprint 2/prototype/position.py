class Position:
    """Positions are represented by a tuple of (x, y) coordinates."""
    
    def __init__(self, x: int, y: int) -> None:
        """Initialize a position with x and y coordinates."""
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        """Returns the x-coordinate of the position."""
        return self._x
    
    @property
    def y(self) -> int:
        """Returns the y-coordinate of the position."""
        return self._y
    