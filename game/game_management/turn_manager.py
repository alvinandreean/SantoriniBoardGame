from typing import List

from core.board import Board
from core.player import Player
from core.worker import Worker
from game_management.sequence import Sequence
from win_conditions.win_condition_strategy import WinConditionStrategy
from game_management.game_phase_manager import GamePhaseManager
from win_conditions.win_condition_checker import WinConditionChecker
from utils.timer_manager import TimerManager

class TurnManager:
    """Coordinates turn flow and player management."""

    def __init__(self, players: List[Player], board: Board, timer_manager: TimerManager, win_condition: WinConditionStrategy) -> None:
        """Initialize the turn manager with players, board, and phase manager and timer manager."""
        self._players = Sequence(players)
        self._board = board
        self._phase_manager = GamePhaseManager()
        self._win_checker = WinConditionChecker(win_condition)
        self._timer_manager = timer_manager
        self.start_turn()
    
    @property
    def current_player(self) -> Player:
        """Return the current player."""
        return self._players.current

    @property
    def worker(self) -> Worker:
        """Return the currently selected worker."""
        return self._phase_manager.current_worker
    
    def get_phase(self) -> str:
        """Get the current game phase."""
        return self._phase_manager.get_current_phase()
    
    def current_phase_optional(self) -> bool:
        """Check if the current phase is optional."""
        return self._phase_manager.is_current_phase_optional()

    def skip_phase(self) -> None:
        """Skip the current phase if it's optional."""
        if self.current_phase_optional():
            self._phase_manager.advance_phase()
    
    def start_turn(self) -> None:
        """Initialize state for a new turn (always Move → Build)."""
        # Create a new action sequence for the current player based on their god card.
        current_player = self.current_player
        
        # Use TimerManager to start player's timer
        if self._timer_manager and current_player:
            self._timer_manager.start_player_timer(current_player)
        
        if current_player and current_player.god_card:
            action_sequence = Sequence(current_player.god_card.get_action_sequence())
            self._phase_manager.initialize_turn(action_sequence)

    def end_turn(self) -> None:
        """End current turn and starts off the next player's turn."""
        
        if self._timer_manager:
            self._timer_manager.pause_current_timer()
            
        # Advance to the next player in the sequence.
        self._players.advance()
        # Reset the index to the first player if we have cycled through all players.
        if self._players.current is None:
            self._players.reset_index()

        # Start the next player's turn.
        self.start_turn()
        
    def set_win_condition_strategy(self, strategy: WinConditionStrategy) -> None:
        """Set the win condition strategy."""
        self._win_checker.strategy = strategy
    
    def get_game_result(self) -> Player | None:
        """Check if there is a winner after the current action."""
        current_player = self.current_player
        current_worker = self._phase_manager.current_worker
        all_players = self._players.items
        
        return self._win_checker.determine_winner(
            all_players, current_player, current_worker, self._board
        )
    

