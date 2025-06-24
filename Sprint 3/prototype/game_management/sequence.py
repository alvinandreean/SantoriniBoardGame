from typing import List
from actions.action_result import ActionResult

class Sequence:
    """A sequence of items that can be iterated over."""
    def __init__(self, items: List[object]) -> None:
        """Initializes the sequence with a list of items."""
        self._items = items.copy()
        self._idx = 0

    @property
    def current(self) -> object | None:
        """Returns the current item in the sequence."""
        return self._items[self._idx] if self._idx < len(self._items) else None

    @property
    def index(self) -> int:
        """Returns the current index in the sequence."""
        return self._idx
    
    @property
    def items(self) -> List[object]:
        """Returns the items in the sequence."""
        return self._items

    def advance(self) -> None:
        """Advances the index to the next item in the sequence."""
        self._idx += 1

    def reset_index(self) -> None:
        """Resets the index to the start of the sequence."""
        self._idx = 0
    
    def handle_action_result(self, result: ActionResult) -> None:
        """
        Handle the result of an action execution.
        If result has additional actions, insert them right after current position.
        This method provides ActionResult support while maintaining backward compatibility.
        """
        # Check if we need to add more actions before advancing
        if result.has_additional_actions():
            # Insert additional actions right after current position
            insert_position = self._idx + 1
            for i, action in enumerate(result.additional_actions):
                self._items.insert(insert_position + i, action)
        
        # Then advance to next action (which might be one of the newly inserted ones)
        self._idx += 1
    
    def is_complete(self) -> bool:
        """Check if sequence is complete."""
        return self._idx >= len(self._items)
    