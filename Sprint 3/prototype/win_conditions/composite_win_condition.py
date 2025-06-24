from typing import List
from core.player import Player
from core.worker import Worker
from core.board import Board
from win_conditions.win_condition_strategy import WinConditionStrategy


class CompositeWinCondition(WinConditionStrategy):
    """
    Composite win condition that combines multiple win condition strategies.
    Enables games to have both standard and timer-based win conditions simultaneously.
    """
    
    def __init__(self, win_conditions: List[WinConditionStrategy]) -> None:
        """Initialize with a list of win condition strategies."""
        self._win_conditions = win_conditions
    
    def add_win_condition(self, win_condition: WinConditionStrategy) -> None:
        """Add a new win condition to the composite."""
        self._win_conditions.append(win_condition)
    
    def remove_win_condition(self, win_condition: WinConditionStrategy) -> None:
        """Remove a win condition from the composite."""
        if win_condition in self._win_conditions:
            self._win_conditions.remove(win_condition)
    
    def check_win(self, player: Player, worker: Worker, board: Board) -> bool:
        """
        Check if player wins under any of the combined win conditions.
        Returns True if ANY win condition is satisfied.
        """
        for win_condition in self._win_conditions:
            if win_condition.check_win(player, worker, board):
                return True
        return False
    
    def check_lose(self, player: Player, board: Board) -> bool:
        """
        Check if player loses under any of the combined win conditions.
        Returns True if ANY lose condition is satisfied.
        """
        for win_condition in self._win_conditions:
            if win_condition.check_lose(player, board):
                return True
        return False 