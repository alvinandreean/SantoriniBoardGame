import random
from typing import List

from god_cards.artemis import Artemis
from god_cards.demeter import Demeter
from god_cards.god_card import GodCard

class GodCardDeck:
    """Represents a deck of god cards for the game."""
    def __init__(self) -> None:
        """Initializes the deck with available cards."""
        self._cards = [
            Artemis(),
            Demeter(),
           
        ]

    def draw(self) -> GodCard:
        """Draws a random god card from the deck."""
        
        # If deck is empty
        if not self._cards: 
            raise ValueError("No more god cards available!")
        
        # Randomly select a card
        card = random.choice(self._cards) 
        # Remove the drawn card from the deck
        self._cards.remove(card) 
        
        return card

    def add_card(self, god_card: GodCard) -> None:
        """Adds a god card back to the deck."""
        self._cards.append(god_card)

    def is_empty(self) -> bool:
        """Checks if the deck is empty."""
        return len(self._cards) == 0

    def remaining(self) -> List[GodCard]:
        """Returns the remaining god cards in the deck."""
        return list(self._cards)