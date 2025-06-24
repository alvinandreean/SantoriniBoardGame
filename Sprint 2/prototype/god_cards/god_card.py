from abc import ABC, abstractmethod
from actions.action import Action
from typing import List

class GodCard(ABC):
    """Abstract base class for god cards."""

    def __init__(self, name: str, description: str = "No description provided."):
        """Initializes a god card with a name and a description."""
        self._name = name
        self._description = description
    
    @property
    def name(self) -> str:
        """Returns the name of the god card."""
        return self._name
    
    @abstractmethod
    def get_action_sequence(self) -> List[Action]:
        """Must be implemented: defines the player's turn sequence."""
        pass
