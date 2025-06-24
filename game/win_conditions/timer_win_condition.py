from core.player import Player
from core.worker import Worker
from core.board import Board
from win_conditions.win_condition_strategy import WinConditionStrategy


class TimerWinCondition(WinConditionStrategy):
    """Timer-based win condition: Player loses if their timer expires."""
    
    def check_win(self, player: Player, worker: Worker, board: Board) -> bool:
        """
        Check if player wins by timer-based condition.
        In timer mode, winning is typically achieved through standard conditions
        (like reaching level 3) rather than timer expiration.
        """
        return False
    
    def check_lose(self, player: Player, board: Board) -> bool:
        """
        Check if player loses due to timer expiration.
        Lose condition: Player's timer has expired.
        """
        return player.timer.is_expired 