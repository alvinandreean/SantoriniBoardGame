import pygame
import sys
from typing import Optional

from colors.color import Color
from core.game import Game
from ui.screen_manager import ScreenManager
from ui.screen_enums import ScreenType
from tutorial.tutorial_ui_adapter import TutorialUIAdapter
from utils.resource_manager import ResourceManager


class SantoriniPygameApp:
    """Main application class using OOP screen-based architecture."""
    
    # Window and board constants
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 1000
    TILE_SIZE = 120
    BOARD_W = 5
    BOARD_H = 5
    FPS = 60
    
   # Color constants (RGB tuples) - Enhanced with modern palette
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (230, 230, 230)
    DARK_GRAY = (64, 64, 64)
    RED = (220, 50, 50)
    LIGHT_RED = (255, 150, 150)
    BLUE = (50, 120, 220)
    LIGHT_BLUE = (150, 200, 255)
    GREEN = (50, 180, 100)
    LIGHT_GREEN = (150, 255, 180)
    YELLOW = (255, 220, 50)
    BROWN = (139, 69, 19)
    PURPLE = (150, 80, 200)
    LIGHT_PURPLE = (200, 150, 255)
    
    # Additional modern colors
    OCEAN_BLUE = (52, 152, 219)
    EMERALD = (46, 204, 113)
    SUNSET_ORANGE = (230, 126, 34)
    CORAL = (255, 107, 107)
    LAVENDER = (155, 89, 182)
    NAVY = (52, 73, 94)
    CREAM = (255, 248, 220)
    GOLD = (241, 196, 15)
    SILVER = (189, 195, 199)
    SHADOW = (44, 62, 80)

    
    def __init__(self):
        """Initialize the Santorini pygame application."""
        self._initialize_pygame()
        self._initialize_fonts()
        self._initialize_game_state()
        self._initialize_ui()
    
    def _initialize_pygame(self) -> None:
        """Initialize pygame and create the window."""
        pygame.init()
        pygame.mixer.init()  # Initialize mixer for music/sound
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Santorini")
        self.clock = pygame.time.Clock()
        self.running = True
    
    def _initialize_fonts(self) -> None:
        """Initialize font objects for different text sizes."""
        self.small_font = pygame.font.Font(None, 20)
        self.medium_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
    
    def _initialize_game_state(self) -> None:
        """Initialize game-related state variables."""
        self.game: Optional[Game] = None
        
        # Setup screen state
        self.game_mode_type = "standard"  # "standard" or "tutorial"
        self.tutorial_type = "basic"  # "basic", "win", "lose"
        self.timer_minutes = 10
        self.active_input = None
        
        # Player configuration
        self.player1_name = ""
        self.player2_name = ""
        self.player1_color = None
        self.player2_color = None
        
        # Tutorial state
        self.tutorial_adapter = TutorialUIAdapter(self)
        self.tutorial_instructions = ""
    
    def _initialize_ui(self) -> None:
        """Initialize the screen management system."""
        self.screen_manager = ScreenManager(self)
        self.screen_manager.change_screen(ScreenType.MAIN_MENU)
        
        # Start background music
        ResourceManager.load_and_play_background_music("assets/music.mp3", volume=0.3)
    
    def run(self) -> None:
        """Main game loop"""
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()
    
    def _handle_events(self) -> None:
        """Handle pygame events by delegating to current screen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.screen_manager.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.screen_manager.handle_keypress(event)
    
    def _update(self) -> None:
        """Update game state by delegating to current screen."""
        self.screen_manager.update()
    
    def _render(self) -> None:
        """Render the current screen."""
        self.screen.fill(self.WHITE)
        self.screen_manager.render(self.screen)
        pygame.display.flip()

    def change_screen(self, screen_type: ScreenType) -> None:
        """Change to a different screen."""
        self.screen_manager.change_screen(screen_type)
    
    def quit_application(self) -> None:
        """Quit the application."""
        self.running = False

    def get_game(self) -> Optional[Game]:
        """Get the current game instance."""
        return self.game
    
    def set_game(self, game: Game) -> None:
        """Set the current game instance."""
        self.game = game
    
    def is_tutorial_mode(self) -> bool:
        """Check if currently in tutorial mode."""
        return self.game_mode_type == "tutorial"

    def get_game_mode_type(self) -> str:
        """Get the current game mode type."""
        return self.game_mode_type
    
    def set_game_mode_type(self, mode_type: str) -> None:
        """Set the game mode type."""
        self.game_mode_type = mode_type
    
    def get_tutorial_type(self) -> str:
        """Get the tutorial type."""
        return self.tutorial_type
    
    def set_tutorial_mode(self, tutorial_type: str) -> None:
        """Set tutorial mode and type."""
        self.game_mode_type = "tutorial"
        self.tutorial_type = tutorial_type
    
    def get_timer_minutes(self) -> int:
        """Get timer duration in minutes."""
        return self.timer_minutes
    
    def set_timer_minutes(self, minutes: int) -> None:
        """Set timer duration in minutes."""
        self.timer_minutes = minutes
    
    def get_active_input(self) -> Optional[str]:
        """Get the currently active input field."""
        return self.active_input
    
    def set_active_input(self, input_field: Optional[str]) -> None:
        """Set the active input field."""
        self.active_input = input_field
    
    def get_player_name(self, player_num: int) -> str:
        """Get player name by number (1 or 2)."""
        if player_num == 1:
            return self.player1_name
        elif player_num == 2:
            return self.player2_name
        return ""
    
    def update_player_name(self, player_num: int, name: str) -> None:
        """Update player name by number."""
        if player_num == 1:
            self.player1_name = name
        elif player_num == 2:
            self.player2_name = name
    
    def get_player_color(self, player_num: int) -> Optional[Color]:
        """Get player color by number."""
        if player_num == 1:
            return self.player1_color
        elif player_num == 2:
            return self.player2_color
        return None
    
    def set_player_color(self, player_num: int, color: Color) -> None:
        """Set player color by number."""
        if player_num == 1:
            self.player1_color = color
        elif player_num == 2:
            self.player2_color = color
    
    def show_message(self, message: str) -> None:
        """Show a message to the user"""
        print(f"MESSAGE: {message}")  # print to console
    
    def get_tutorial_adapter(self) -> TutorialUIAdapter:
        """Get the tutorial adapter for tutorial events."""
        return self.tutorial_adapter
    
    def get_tutorial_instructions(self) -> str:
        """Get current tutorial instructions."""
        return self.tutorial_instructions
    
    def update_tutorial_ui(self) -> None:
        """Update tutorial UI elements."""
        if self.game and self.is_tutorial_mode():
            # Get current game state for progression
            current_player = self.game.turn_manager.current_player
            current_worker = self.game.turn_manager.worker
            current_phase = self.game.get_current_phase()
            
            self.game.game_mode.handle_post_action_update(
                current_player, current_worker, current_phase, self.game.board
            )
            
            tutorial_manager = self.game.game_mode.tutorial_manager
            self.tutorial_instructions = tutorial_manager.get_current_instructions()
    
    def handle_tutorial_board_click(self, board_x: int, board_y: int) -> None:
        """Handle board clicks in tutorial mode."""
        if self.game and self.is_tutorial_mode():
            tutorial_manager = self.game.game_mode.tutorial_manager
            current_step = tutorial_manager.get_current_step()
            
            # Get the tile that was clicked
            from core.position import Position
            tile = self.game.board.get_tile(Position(board_x, board_y))
            
            # Get current game state
            current_player = self.game.turn_manager.current_player
            current_worker = self.game.turn_manager.worker
            phase = self.game.turn_manager.get_phase()
            
            current_step.handle_tile_click(tile, current_player, current_worker, phase)
            self.update_tutorial_ui()
    
    def handle_game_over(self, result: str) -> None:
        """Handle game over scenarios by showing the game over screen."""
        
        # Set the game result in the game over screen
        game_over_screen = self.screen_manager.get_game_over_screen()
        game_mode = "tutorial" if self.is_tutorial_mode() else "standard"
        game_over_screen.set_game_result(result, game_mode)
        
        # Change to game over screen
        self.change_screen(ScreenType.GAME_OVER)


def main():
    """Entry point for the Santorini application."""
    app = SantoriniPygameApp()
    app.run()


if __name__ == "__main__":
    main() 