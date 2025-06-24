from abc import ABC, abstractmethod

from core.player import Player
from core.worker import Worker
from core.board import Board


class WinConditionStrategy(ABC):
    """Abstract strategy for different win condition types."""
    
    @abstractmethod
    def check_win(self, player: Player, worker: Worker, board: Board) -> bool:
        """Check if the given player has won under this win condition."""
        pass
    
    @abstractmethod
    def check_lose(self, player: Player, board: Board) -> bool:
        """Check if the given player has lost under this win condition."""
        pass 