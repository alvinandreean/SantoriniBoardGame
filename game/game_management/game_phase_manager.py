from typing import Optional, TYPE_CHECKING

from game_management.sequence import Sequence
from core.worker import Worker

if TYPE_CHECKING:
    from actions.action_result import ActionResult


class GamePhaseManager:
    """
    Manages game phases and action sequences.
    
    Encapsulates phase state and transitions.
    """
    
    def __init__(self) -> None:
        """Initialize the phase manager."""
        self._actions: Optional[Sequence] = None
        self._worker: Optional[Worker] = None
    
    @property
    def current_worker(self) -> Optional[Worker]:
        """Get the currently selected worker."""
        return self._worker
    
    @current_worker.setter
    def current_worker(self, worker: Optional[Worker]) -> None:
        """Set the currently selected worker."""
        self._worker = worker
    
    @property
    def action_sequence(self) -> Optional[Sequence]:
        """Get the current action sequence."""
        return self._actions
    
    def initialize_turn(self, action_sequence: Sequence) -> None:
        """Initialize a new turn with the given action sequence."""
        self._actions = action_sequence
        self._worker = None
    
    def get_current_phase(self) -> str:
        """
        Get the current game phase.
        Returns current phase as string: "Select Worker", "Move", "Build", "End Turn".
        """
        if self._worker is None:
            return "Select Worker"
        
        if self._actions is None:
            return "End Turn"
            
        current_action = self._actions.current
        if current_action is None:
            return "End Turn"
            
        return current_action.get_name()
    
    def is_current_phase_optional(self) -> bool:
        """Check if the current phase is optional."""
        if self._actions is None:
            return False
            
        current_action = self._actions.current
        if current_action is None:
            return False
            
        return current_action.optional
    
    def handle_action_result(self, result: 'ActionResult') -> None:
        """Handle ActionResult from action execution (supports dynamic action insertion)."""
        if self._actions is not None:
            self._actions.handle_action_result(result)
    
    def advance_phase(self) -> None:
        """Advance to the next phase in the action sequence (legacy method)."""
        if self._actions is not None:
            self._actions.advance()
    
    def is_turn_complete(self) -> bool:
        """Check if the current turn is complete."""
        if self._actions is None:
            return True
            
        return self._actions.current is None
    
    def get_current_action(self) -> None:
        """Get the current action to be performed."""
        if self._actions is None:
            return None
            
        return self._actions.current
    
    def has_worker_selected(self) -> bool:
        """Check if a worker is currently selected."""
        return self._worker is not None 