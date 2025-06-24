from typing import List, Optional

from core.player import Player
from core.worker import Worker
from core.board import Board
from win_conditions.win_condition_strategy import WinConditionStrategy
from win_conditions.standard_win_condition import StandardWinCondition


class WinConditionChecker:
    """Manages win/lose condition checking using Strategy pattern."""
    
    def __init__(self, strategy: WinConditionStrategy = None) -> None:
        """Initialize with a win condition strategy."""
        self._strategy = strategy or StandardWinCondition()
    
    @property
    def strategy(self) -> WinConditionStrategy:
        """Get the current win condition strategy."""
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: WinConditionStrategy) -> None:
        """Change the win condition strategy."""
        self._strategy = strategy
    
    def check_win(self, player: Player, worker: Worker, board: Board) -> bool:
        """Check if the given player has won."""
        return self._strategy.check_win(player, worker, board)
    
    def check_lose(self, player: Player, board: Board) -> bool:
        """Check if the given player has lost."""
        return self._strategy.check_lose(player, board)
    
    def determine_winner(self, players: List[Player], current_player: Player, 
                        worker: Worker, board: Board) -> Optional[Player]:
        """
        Determine if there is a winner after a game action.
        Returns winning player if game is over, None if game continues.
        """
        # Check if current player wins
        if self.check_win(current_player, worker, board):
            return current_player
            
        # Check if current player loses (no valid moves)
        if self.check_lose(current_player, board):
            # Find next player as winner
            current_index = players.index(current_player)
            winner_index = (current_index + 1) % len(players)
            return players[winner_index]
            
        return None  # Game continues 