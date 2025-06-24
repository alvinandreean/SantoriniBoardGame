from typing import List
from god_cards.god_card  import GodCard
from actions.action import Action 
from actions.move_action import MoveAction
from actions.build_action import BuildAction
from actions.artemis_move_action import ArtemisMoveAction

class Artemis(GodCard):
    """Artemis gives the player an additional move action each turn."""

    def __init__(self) -> None:
        """Initializes the Artemis god card."""
        super().__init__("Artemis")
        self._description = "You may move one additional time, but not back to the space you just left."

    def get_action_sequence(self) -> List[Action]:
        return [
            MoveAction(),
            ArtemisMoveAction(optional= True),
            BuildAction()
        ]