from typing import List

from board import Board
from player import Player
from worker import Worker
from sequence import Sequence
from validator import Validator
from tile import Tile

class TurnManager:
    """Drives the turn flow: select, move, build, and god powers."""

    def __init__(self, players: List[Player], board: Board) -> None:
        """
        Initializes the turn manager with players and board
        
        Each player has a god card that determines the action sequence.
        The turn manager handles the flow of the game, including selecting workers,
        moving them, building, and using god powers.
        

        """
        self._players = Sequence(players)
        self._board = board
        self._actions: Sequence = None
        self._worker = None

        self.start_turn()
    
    @property
    def current_player(self) -> Player:
        """Return the current player."""
        return self._players.current

    @property
    def worker(self) -> Worker:
        """Return the currently selected worker."""
        return self._worker
    
    def get_phase(self) -> str:
        """
        Returns the current phase:
          - "Select Worker" (haven’t picked yet)
          - "Move" (next step is a MoveAction)
          - "Build" (next step is a BuildAction)
          - "End Turn" (no more steps)
        """
        if self._worker is None:
            return "Select Worker"

        step = self._actions.current
        if step is None:
            return "End Turn"

        return step.get_name()
    
    def current_phase_optional(self) -> bool:
        """Returns True if the current phase is optional."""
        # Check if there is a current action in the sequence.
        current = self._actions.current
        if current is None:
            return False
        else:
            return current.optional

    def skip_phase(self) -> None:
        """Skip the current phase."""
        # Advance the action sequence to skip the current phase.
        self._actions.advance()
    
    def start_turn(self) -> None:
        """Initialize state for a new turn (always Move → Build)."""
        # Create a new action sequence for the current player based on their god card.
        self._actions = Sequence(self.current_player.god_card.get_action_sequence())
        # Reset the selected worker.
        self._worker = None

    def end_turn(self) -> None:
        """End current turn and starts off the next player's turn."""
        # Advance to the next player in the sequence.
        self._players.advance()
        # Reset the index to the first player if we have cycled through all players.
        if self._players.current is None:
            self._players.reset_index()

        # Start the next player's turn.
        self.start_turn()
        
        
    def check_win(self) -> Player | None:
        """Check if the current player has won the game."""
        
        # Check if there is a selected worker.
        if not self._worker:
            return None

        # Get the current tile and its building level.
        current_tile = self._board.get_tile(self._worker.position)
        building = current_tile.building
        # Check if the building is level 3.
        if not building or building.level != 3:
            return None

        # Get the previous position of the worker and its building level.
        prev_pos = self._worker.previous_position
        prev_tile = self._board.get_tile(prev_pos) if prev_pos else None
        prev_level = (prev_tile.building.level
                      if prev_tile and prev_tile.building else 0)

        # Check if the previous building level was 2.
        # If the previous building level was 2, the current player wins.
        if prev_level == 2:
            return self.current_player
        return None
    
    def check_lose(self, movable_workers: List[Worker]) -> Player | None:
        """Check if the current player has lost the game."""
        
        # Iterate through the workers of the current player.
        for worker in movable_workers:
            # Get the valid move tiles for each worker.
            valid_moves = Validator.get_valid_move_tiles(worker, self._board)
            # If there are still valid moves for any worker, the game continues.
            if valid_moves:
                return None  # At least one worker can move

        # Else, the current player has lost because no workers can move.
        players = self._players.items
        current = self._players.index
        # Get the next player in the sequence.
        winner_index = (current + 1) % len(players)
        # Declare the next player as the winner.
        return players[winner_index]
    
    def get_game_result(self) -> Player | None:
        """Check if anyone has won or lost, after a click."""
        
        # 1. Check if current player wins (level 3 move)
        winner = self.check_win()
        if winner:
            return winner

        winner = self.check_lose(self._players.current.all_workers)
        if winner:
            return winner

        return None  
    
    def handle_click(self, tile: Tile) -> None:
        """Handle a click on a tile."""
        
        # Select a worker if none is selected.
        if self._worker is None:
            # Check if any worker can still move.
            if tile.worker in self.current_player.workers:
                valid_moves = Validator.get_valid_move_tiles(tile.worker, self._board)
                # Touch-Move: Select the worker if it has valid moves.
                # If the worker has valid moves, select it.
                # If the worker has no valid moves, do not select it.
                if valid_moves:
                    self._worker = tile.worker
            return

        # Get the current action
        action = self._actions.current
        # If there are no actions left, end the turn.
        if action is None:
            self.end_turn()
            return

        # Validate the action
        if not action.validate(self._worker, self._board, tile):
            return

        # Execute the action
        action.execute(self._worker, self._board, tile)
        
        # Advance the action sequence to the next action.
        self._actions.advance()

