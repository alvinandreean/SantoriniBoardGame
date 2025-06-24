from enum import Enum, auto

class Color(Enum):
    """ 
    Enumeration for the colors of players in the game.
    
    Each player is assigned a color, which can be used to identify the workers in the game.
    """
    RED = auto()
    BLUE = auto()