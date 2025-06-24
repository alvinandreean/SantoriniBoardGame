from enum import Enum


class ScreenType(Enum):
    """Enumeration of all available screen types."""
    MAIN_MENU = "main_menu"
    TUTORIAL_SELECTION = "tutorial_selection"
    SETUP = "setup"
    GAME = "game"
    GAME_OVER = "game_over" 