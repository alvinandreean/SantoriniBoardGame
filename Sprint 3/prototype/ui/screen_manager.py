from typing import Dict, Optional
from ui.base_screen import BaseScreen
from ui.screen_enums import ScreenType
from ui.main_menu_screen import MainMenuScreen
from ui.tutorial_selection_screen import TutorialSelectionScreen
from ui.setup_screen import SetupScreen
from ui.game_screen import GameScreen
from ui.game_over_screen import GameOverScreen


class ScreenManager:
    """Manages screen instances and transitions following OOP principles."""
    
    def __init__(self, app):
        """Initialize screen manager with reference to main application."""
        self.app = app
        self.current_screen: Optional[BaseScreen] = None
        self.screens: Dict[ScreenType, BaseScreen] = {}
        self._initialize_screens()
    
    def _initialize_screens(self) -> None:
        """Create instances of all screen types."""
        self.screens[ScreenType.MAIN_MENU] = MainMenuScreen(self.app)
        self.screens[ScreenType.TUTORIAL_SELECTION] = TutorialSelectionScreen(self.app)
        self.screens[ScreenType.SETUP] = SetupScreen(self.app)
        self.screens[ScreenType.GAME] = GameScreen(self.app)
        self.screens[ScreenType.GAME_OVER] = GameOverScreen(self.app)
    
    def change_screen(self, screen_type: ScreenType) -> None:
        """Change to a different screen with proper lifecycle management."""
        # Exit current screen
        if self.current_screen:
            self.current_screen.on_exit()
        
        # Get new screen
        new_screen = self.screens.get(screen_type)
        if not new_screen:
            raise ValueError(f"Screen type {screen_type} not found")
        
        # Enter new screen
        self.current_screen = new_screen
        self.current_screen.on_enter()
    
    def handle_click(self, pos) -> None:
        """Delegate click handling to current screen."""
        if self.current_screen:
            self.current_screen.handle_click(pos)
    
    def handle_keypress(self, event) -> None:
        """Delegate keyboard input to current screen."""
        if self.current_screen:
            self.current_screen.handle_keypress(event)
    
    def update(self) -> None:
        """Update current screen state."""
        if self.current_screen:
            self.current_screen.update()
    
    def render(self, surface) -> None:
        """Render current screen."""
        if self.current_screen:
            self.current_screen.render(surface)
    
    def get_current_screen_type(self) -> Optional[ScreenType]:
        """Get the type of the current screen."""
        for screen_type, screen in self.screens.items():
            if screen is self.current_screen:
                return screen_type
        return None

    def get_game_over_screen(self) -> GameOverScreen:
        """Get the game over screen instance."""
        return self.screens[ScreenType.GAME_OVER] 