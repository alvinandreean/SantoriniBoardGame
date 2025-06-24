from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from actions.action import Action



class ActionResult:
    """Result of action execution. Empty = continue normally, with actions = add them."""
    
    def __init__(self, additional_actions: List['Action'] = None):
        self._additional_actions: List['Action'] = additional_actions or []

    @property
    def additional_actions(self) -> List['Action']:
        """Get the additional actions."""
        return self._additional_actions
    
    def has_additional_actions(self) -> bool:
        """Check if this result contains additional actions to add."""
        return len(self.additional_actions) > 0
    
    def is_empty(self) -> bool:
        """Check if this is an empty result (continue normally)."""
        return len(self.additional_actions) == 0 