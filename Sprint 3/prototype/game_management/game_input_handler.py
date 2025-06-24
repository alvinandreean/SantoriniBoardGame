from typing import Optional

from core.tile import Tile
from utils.validator import Validator
from game_management.turn_manager import TurnManager

class GameInputHandler:
    """
    Handles game input interactions and UI logic.

    Separates UI concerns from core game logic.
    """
    
    def __init__(self, turn_manager: TurnManager) -> None:
        """Initialize with a reference to the turn manager."""
        self._turn_manager = turn_manager
    
    def handle_tile_click(self, tile: Tile) -> Optional[str]:
        """
        Handle a click on a game tile.
        Returns feedback message for UI display, or None if no feedback needed.
        """
        # Handle worker selection if none selected
        if not self._turn_manager._phase_manager.has_worker_selected():
            return self._handle_worker_selection(tile)
        
        # Handle action execution if worker is selected
        return self._handle_action_execution(tile)
    
    def _handle_worker_selection(self, tile: Tile) -> Optional[str]:
        """Handle worker selection logic and return feedback."""
        current_player = self._turn_manager.current_player
        board = self._turn_manager._board
        
        # Check if tile has a worker
        if not tile.has_worker():
            return "Please select a tile with your worker."
        
        # Check if tile contains player's worker
        if tile.worker not in current_player.workers:
            return "You can only select your own workers."
            
        # Check if worker has valid moves (touch-move rule)
        valid_moves = Validator.get_valid_move_tiles(tile.worker, board)
        if not valid_moves:
            return "This worker has no valid moves."
            
        # Select the worker
        self._turn_manager._phase_manager.current_worker = tile.worker
        return f"Worker selected. Current phase: {self._turn_manager.get_phase()}"
    
    def _handle_action_execution(self, tile: Tile) -> Optional[str]:
        """Handle action execution logic and return feedback."""
        # Check if turn is complete
        if self._turn_manager._phase_manager.is_turn_complete():
            self._turn_manager.end_turn()
            current_player = self._turn_manager.current_player
            return f"Turn ended. Now {current_player.player_name}'s turn."
        
        # Get current action
        current_action = self._turn_manager._phase_manager.get_current_action()
        if current_action is None:
            self._turn_manager.end_turn()
            current_player = self._turn_manager.current_player
            return f"Turn ended. Now {current_player.player_name}'s turn."
        
        # Validate action
        current_worker = self._turn_manager._phase_manager.current_worker
        board = self._turn_manager._board
        
        if not current_action.validate(current_worker, board, tile):
            action_name = current_action.get_name()
            return f"Invalid {action_name.lower()}. Please try again."
        
        # Execute action
        result = current_action.execute(current_worker, board, tile)
        
        # Handle the ActionResult (this will add additional actions if needed)
        self._turn_manager._phase_manager.handle_action_result(result)
        
        # Provide feedback about next phase
        next_phase = self._turn_manager.get_phase()
        if next_phase == "End Turn":
            return f"{current_action.get_name()} completed."
        else:
            return f"{current_action.get_name()} completed. Next: {next_phase}" 