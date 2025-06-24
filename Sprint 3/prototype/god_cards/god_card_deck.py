import random
from typing import List

from god_cards.god_card import GodCard
from god_cards.god_card_factory import GodCardFactory

class GodCardDeck:
    """
    Represents a deck of god cards for the game.
    
    Now uses GodCardFactory for better extensibility.
    Adding new god cards only requires registering them with the factory.
    """
    
    def __init__(self, card_names: List[str]) -> None:
        """Initializes the deck with available cards."""
        # Create instances of all specified cards
        self._cards = []
        for card_name in card_names:
            try:
                card = GodCardFactory.create_card(card_name)
                
                self._cards.append(card)
            except ValueError as e:
                print(f"Warning: Skipping unknown card '{card_name}': {e}")
        
        if not self._cards:
            raise ValueError("No valid god cards available in deck!")

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
    
    def remaining_count(self) -> int:
        """Returns the number of remaining god cards."""
        return len(self._cards)
    
    def peek_remaining_names(self) -> List[str]:
        """Returns the names of remaining god cards without drawing them."""
        return [card.name for card in self._cards]