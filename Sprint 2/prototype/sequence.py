from typing import List

class Sequence:
    """A sequence of items that can be iterated over."""
    def __init__(self, items: List[object]) -> None:
        """Initializes the sequence with a list of items."""
        self._items = items
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
    