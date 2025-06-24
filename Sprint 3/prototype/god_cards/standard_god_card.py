from typing import List

from god_cards.god_card import GodCard
from actions.action import Action
from actions.move_action import MoveAction
from actions.build_action import BuildAction


class StandardGodCard(GodCard):
    """
    Standard god card for tutorial mode.
    Provides basic move and build actions without special powers.
    """
    
    def __init__(self) -> None:
        """Initialize standard god card."""
        super().__init__(
            name="Standard",
            description="Basic Santorini gameplay: Move one worker, then build."
        )
    
    def get_action_sequence(self) -> List[Action]:
        """Return standard action sequence: Move then Build."""
        return [
            MoveAction(),
            BuildAction()
        ] 