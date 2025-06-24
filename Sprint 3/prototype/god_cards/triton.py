from god_cards.god_card import GodCard
from actions.action import Action
from actions.triton_move_action import TritonMoveAction
from actions.build_action import BuildAction
from typing import List



class Triton(GodCard):
    """Triton allows worker to move again after moving into a perimeter space."""
    
    def __init__(self):
        """Initialize the Triton god card."""
        super().__init__(
            name="Triton",
            description="Each time your Worker moves into a perimeter space, it may immediately move again."
        )
    
    def get_action_sequence(self) -> List[Action]:
        """Return the action sequence with Triton's special move action."""
        return [
            TritonMoveAction(),  
            BuildAction()        
        ] 