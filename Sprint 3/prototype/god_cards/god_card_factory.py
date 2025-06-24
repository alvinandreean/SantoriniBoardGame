from typing import Dict, Type, List, Optional
from god_cards.god_card import GodCard
from god_cards.artemis import Artemis
from god_cards.demeter import Demeter
from god_cards.triton import Triton

class GodCardFactory:
    """
    Factory for creating god cards.
    
    Implements the Factory Pattern to make adding new god cards easier
    """
    
    # Registry of available god cards
    _registered_cards: Dict[str, Type[GodCard]] = {}
    
    @classmethod
    def register_card(cls, name: str, card_class: Type[GodCard]) -> None:
        """Registers a new god card type with the factory."""
        cls._registered_cards[name.lower()] = card_class
    
    @classmethod
    def create_card(cls, name: str) -> GodCard:
        """Creates a god card instance by name."""
        name_lower = name.lower()
        if name_lower not in cls._registered_cards:
            available = ', '.join(cls._registered_cards.keys())
            raise ValueError(f"Unknown god card: '{name}'. Available: {available}")
        
        card_class = cls._registered_cards[name_lower]
        return card_class()
    
    @classmethod
    def get_available_card_names(cls) -> List[str]:
        """Returns a list of all available god card names."""
        return list(cls._registered_cards.keys())

    
GodCardFactory.register_card("Artemis", Artemis)
GodCardFactory.register_card("Demeter", Demeter)
GodCardFactory.register_card("Triton", Triton)
