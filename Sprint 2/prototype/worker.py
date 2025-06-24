from position import Position
from colors.color import Color

class Worker:
    """ Represents a worker in the Santorini game. """

    def __init__(self, initial_position: Position, color: Color) -> None:
        """Initializes a worker with a given position and color."""
        self._position = initial_position
        self._color = color
        self._previous_position = None
        self._previous_build_pos = None

    @property
    def position(self) -> Position:
        """Returns the current position of the worker."""
        return self._position

    @position.setter
    def position(self, new_position: Position) -> None:
        """Sets a new position for the worker."""
        self._previous_position = self._position
        self._position = new_position

    @property
    def previous_position(self) -> Position | None:
        """Returns the previous position of the worker."""
        return self._previous_position
    
    @property
    def previous_build_pos(self) -> Position | None:
        """Returns the previous build position of the worker."""
        return self._previous_build_pos
    
    @previous_build_pos.setter
    def previous_build_pos(self, new_position: Position) -> None:
        """Sets a new build position for the worker."""
        self._previous_build_pos = new_position
