from abc import ABC, abstractmethod
from worker import Worker
from board import Board
from tile import Tile


class Action(ABC):
    """Base action class to implemens phases/actions a player can do in a turn."""

    def __init__(self, optional: bool = False):
        self._optional = optional

    @abstractmethod
    def execute(self, worker: Worker, board: Board, target: Tile) -> None:
        """Mutate the board by moving or building."""
        pass

    def validate(self, worker: Worker, board: Board, tile: Tile) -> bool:
        """
        Return True if this action *can* be applied to (worker,board,tile).
        Default = always valid; subclasses override.
        """
        return True
    
    @property
    def optional(self) -> bool:
        """Return True if this action is optional."""
        return self._optional

    def get_name(self) -> str:
        """Returns name of current action as string for UI display."""
        classname = self.__class__.__name__
        if classname.endswith("Action"):
            base_name = classname[:-6]  # remove "Action" (6 letters)
        else:
            base_name = classname
        if self._optional:
            return base_name  # optional actions, full base name
        else:
            return base_name
