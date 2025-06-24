from typing import List

from god_cards.god_card import GodCard
from actions.action import Action
from actions.move_action import MoveAction
from actions.build_action import BuildAction
from actions.demeter_build_action import DemeterBuildAction

class Demeter(GodCard):
    """Demeter gives player an additional build action each turn."""

    def __init__(self) -> None:
        """Initializes the Demeter god card."""
        super().__init__("Demeter")
        self._description = "You may build one additional time, but not on the same space."

    def get_action_sequence(self) -> List[Action]:
        return [
            MoveAction(),
            BuildAction(),
            DemeterBuildAction(optional= True)
        ]