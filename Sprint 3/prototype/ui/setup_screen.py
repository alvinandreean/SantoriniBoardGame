from typing import Tuple
import pygame
from ui.base_screen import BaseScreen
from ui.screen_enums import ScreenType
from colors.color import Color
from core.player import Player
from core.game import Game
from game_modes.standard_game_mode import StandardGameMode
from game_modes.tutorial_game_mode import TutorialGameMode
from utils.resource_manager import ResourceManager

class SetupScreen(BaseScreen):
    """Game setup screen for configuring players and starting games."""
    
    def __init__(self, app):
        """Initialize the setup screen."""
        super().__init__(app)
        self.background_image = None
        self._load_assets()
    
    def _load_assets(self):
        """Load background image and other assets."""
        self.background_image = ResourceManager.load_image("assets/setup.png")
        # Scale background to fit window
        if self.background_image:
            self.background_image = pygame.transform.scale(
                self.background_image, 
                (self.app.WINDOW_WIDTH, self.app.WINDOW_HEIGHT)
            )
    
    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle clicks on setup screen elements."""
        x, y = pos
        
        # Back button
        if self._handle_back_button_click(pos):
            return
        
        # Game mode selection
        if self._handle_mode_selection_click(pos):
            return
        
        # Mode-specific clicks
        if self.app.get_game_mode_type() == "standard":
            self._handle_standard_mode_clicks(pos)
        
        # Start Game button
        if self._handle_start_button_click(pos):
            return
    
    def _handle_back_button_click(self, pos: Tuple[int, int]) -> bool:
        """Handle back button click."""
        back_rect = pygame.Rect(50, 50, 100, 40)
        if back_rect.collidepoint(pos):
            self.app.change_screen(ScreenType.MAIN_MENU)
            return True
        return False
    
    def _handle_mode_selection_click(self, pos: Tuple[int, int]) -> bool:
        """Handle game mode selection button clicks."""
        standard_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 270, 180, 40)
        tutorial_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 + 20, 270, 180, 40)
        
        if standard_rect.collidepoint(pos):
            self.app.set_game_mode_type("standard")
            return True
        elif tutorial_rect.collidepoint(pos):
            self.app.set_game_mode_type("tutorial")
            return True
        return False
    
    def _handle_standard_mode_clicks(self, pos: Tuple[int, int]) -> None:
        """Handle clicks specific to standard mode setup."""
        self._handle_timer_selection_click(pos)
        self._handle_name_input_click(pos)
        self._handle_color_selection_click(pos)
    
    def _handle_timer_selection_click(self, pos: Tuple[int, int]) -> None:
        """Handle timer duration selection clicks."""
        timer_5_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 120, 388, 70, 30)
        timer_10_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 35, 388, 70, 30)
        timer_15_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 + 50, 388, 70, 30)
        
        if timer_5_rect.collidepoint(pos):
            self.app.set_timer_minutes(5)
        elif timer_10_rect.collidepoint(pos):
            self.app.set_timer_minutes(10)
        elif timer_15_rect.collidepoint(pos):
            self.app.set_timer_minutes(15)
    
    def _handle_name_input_click(self, pos: Tuple[int, int]) -> None:
        """Handle player name input field clicks."""
        p1_name_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 150, 490, 300, 30)  # Player 1 at y_offset=460 + 30
        p2_name_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 150, 660, 300, 30)  # Player 2 at y_offset=630 + 30
        
        if p1_name_rect.collidepoint(pos):
            self.app.set_active_input("player1_name")
        elif p2_name_rect.collidepoint(pos):
            self.app.set_active_input("player2_name")
        else:
            self.app.set_active_input(None)
    
    def _handle_color_selection_click(self, pos: Tuple[int, int]) -> None:
        """Handle color selection button clicks."""
        # Player 1 colors (y_offset=460 + 110 = 570)
        p1_red_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 100, 570, 80, 30)
        p1_blue_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 + 20, 570, 80, 30)
        
        if p1_red_rect.collidepoint(pos):
            self.app.set_player_color(1, Color.RED)
        elif p1_blue_rect.collidepoint(pos):
            self.app.set_player_color(1, Color.BLUE)
        
        # Player 2 colors (y_offset=630 + 110 = 740)
        p2_red_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 100, 740, 80, 30)
        p2_blue_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 + 20, 740, 80, 30)
        
        if p2_red_rect.collidepoint(pos):
            self.app.set_player_color(2, Color.RED)
        elif p2_blue_rect.collidepoint(pos):
            self.app.set_player_color(2, Color.BLUE)
    
    def _handle_start_button_click(self, pos: Tuple[int, int]) -> bool:
        """Handle start game button click."""
        start_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 100, 800, 200, 50)
        if start_rect.collidepoint(pos):
            self._start_game()
            return True
        return False
    
    def handle_keypress(self, event: pygame.event.Event) -> None:
        """Handle keyboard input for text fields."""
        if self.app.get_active_input() and self.app.get_game_mode_type() == "standard":
            self._handle_text_input(event)
    
    def _handle_text_input(self, event: pygame.event.Event) -> None:
        """Handle text input for player names."""
        active_input = self.app.get_active_input()
        
        if event.key == pygame.K_BACKSPACE:
            if active_input == "player1_name":
                self.app.update_player_name(1, self.app.get_player_name(1)[:-1])
            elif active_input == "player2_name":
                self.app.update_player_name(2, self.app.get_player_name(2)[:-1])
        else:
            char = event.unicode
            if char.isprintable() and len(char) == 1:
                if active_input == "player1_name" and len(self.app.get_player_name(1)) < 20:
                    self.app.update_player_name(1, self.app.get_player_name(1) + char)
                elif active_input == "player2_name" and len(self.app.get_player_name(2)) < 20:
                    self.app.update_player_name(2, self.app.get_player_name(2) + char)
    
    def update(self) -> None:
        """Setup screen has no continuous updates."""
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the setup screen."""
        self._render_background(surface)
        self._render_back_button(surface)
        self._render_title(surface)
        self._render_mode_selection(surface)
        
        if self.app.get_game_mode_type() == "standard":
            self._render_standard_setup(surface)
        else:
            self._render_tutorial_setup(surface)
        
        self._render_start_button(surface)
    
    def _render_background(self, surface: pygame.Surface) -> None:
        """Render the background image or fallback to solid color."""
        if self.background_image:
            # Use the loaded setup background image
            surface.blit(self.background_image, (0, 0))
        else:
            # Fallback to solid color if image loading failed
            surface.fill(self.app.WHITE)
    
    def _render_back_button(self, surface: pygame.Surface) -> None:
        """Render the back button with modern styling."""
        back_rect = pygame.Rect(50, 50, 100, 40)
        
        # Button shadow
        shadow_rect = pygame.Rect(back_rect.x + 2, back_rect.y + 2, back_rect.width, back_rect.height)
        pygame.draw.rect(surface, self.app.SHADOW, shadow_rect, border_radius=10)
        
        # Main button
        pygame.draw.rect(surface, self.app.CORAL, back_rect, border_radius=10)
        pygame.draw.rect(surface, self.app.BLACK, back_rect, 2, border_radius=10)
        
        # Button text
        back_text = self.app.medium_font.render("Back", True, self.app.WHITE)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        surface.blit(back_text, back_text_rect)
    
    def _render_title(self, surface: pygame.Surface) -> None:
        """Render the screen title with background panel."""
        # Semi-transparent panel behind title
        title_panel = pygame.Rect(self.app.WINDOW_WIDTH//2 - 150, 160, 300, 60)
        panel_surface = pygame.Surface((title_panel.width, title_panel.height))
        panel_surface.set_alpha(180)  # Semi-transparent
        panel_surface.fill((255, 255, 255))  # White background
        surface.blit(panel_surface, title_panel)
        pygame.draw.rect(surface, self.app.BLACK, title_panel, 2)
        
        # Title text (no shadow)
        title_text = self.app.large_font.render("Game Setup", True, self.app.NAVY)
        title_rect = title_text.get_rect(center=(self.app.WINDOW_WIDTH//2, 190))
        surface.blit(title_text, title_rect)
    
    def _render_mode_selection(self, surface: pygame.Surface) -> None:
        """Render game mode selection buttons with modern styling."""
        # Semi-transparent panel for mode selection
        mode_panel = pygame.Rect(self.app.WINDOW_WIDTH//2 - 220, 240, 440, 90)
        panel_surface = pygame.Surface((mode_panel.width, mode_panel.height))
        panel_surface.set_alpha(160)
        panel_surface.fill((255, 255, 255))
        surface.blit(panel_surface, mode_panel)
        pygame.draw.rect(surface, self.app.BLACK, mode_panel, 2)
        
        # Mode label (no shadow)
        mode_label = self.app.medium_font.render("Game Mode:", True, self.app.NAVY)
        mode_rect = mode_label.get_rect(center=(self.app.WINDOW_WIDTH//2, 258))
        surface.blit(mode_label, mode_rect)
        
        # Standard mode button with modern styling
        standard_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 270, 180, 40)
        standard_color = self.app.EMERALD if self.app.get_game_mode_type() == "standard" else self.app.LIGHT_GRAY
        pygame.draw.rect(surface, standard_color, standard_rect, border_radius=10)
        pygame.draw.rect(surface, self.app.BLACK, standard_rect, 2, border_radius=10)
        
        standard_text = self.app.medium_font.render("Standard", True, self.app.WHITE if self.app.get_game_mode_type() == "standard" else self.app.BLACK)
        standard_text_rect = standard_text.get_rect(center=standard_rect.center)
        surface.blit(standard_text, standard_text_rect)
        
        # Tutorial mode button with modern styling
        tutorial_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 + 20, 270, 180, 40)
        tutorial_color = self.app.LAVENDER if self.app.get_game_mode_type() == "tutorial" else self.app.LIGHT_GRAY
        pygame.draw.rect(surface, tutorial_color, tutorial_rect, border_radius=10)
        pygame.draw.rect(surface, self.app.BLACK, tutorial_rect, 2, border_radius=10)
        
        tutorial_text = self.app.medium_font.render("Tutorial", True, self.app.WHITE if self.app.get_game_mode_type() == "tutorial" else self.app.BLACK)
        tutorial_text_rect = tutorial_text.get_rect(center=tutorial_rect.center)
        surface.blit(tutorial_text, tutorial_text_rect)
    
    def _render_standard_setup(self, surface: pygame.Surface) -> None:
        """Render standard game mode setup elements."""
        self._render_timer_selection(surface)
        self._render_player_setup(surface)
    
    def _render_timer_selection(self, surface: pygame.Surface) -> None:
        """Render timer duration selection with background panel."""
        # Semi-transparent panel for timer section
        timer_panel = pygame.Rect(self.app.WINDOW_WIDTH//2 - 170, 350, 340, 80)
        panel_surface = pygame.Surface((timer_panel.width, timer_panel.height))
        panel_surface.set_alpha(160)
        panel_surface.fill((255, 255, 255))
        surface.blit(panel_surface, timer_panel)
        pygame.draw.rect(surface, self.app.BLACK, timer_panel, 2)
        
        # Duration label (no shadow)
        duration_label = self.app.medium_font.render("Timer Duration:", True, self.app.NAVY)
        surface.blit(duration_label, (self.app.WINDOW_WIDTH//2 - 150, 358))
        
        # Timer buttons with modern styling
        timer_options = [(5, -120), (10, -35), (15, 50)]
        for minutes, x_offset in timer_options:
            timer_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 + x_offset, 388, 70, 30)
            timer_color = self.app.EMERALD if self.app.get_timer_minutes() == minutes else self.app.LIGHT_GRAY
            pygame.draw.rect(surface, timer_color, timer_rect, border_radius=8)
            pygame.draw.rect(surface, self.app.BLACK, timer_rect, 2, border_radius=8)
            
            timer_text = self.app.small_font.render(f"{minutes} min", True, self.app.WHITE if self.app.get_timer_minutes() == minutes else self.app.BLACK)
            timer_text_rect = timer_text.get_rect(center=timer_rect.center)
            surface.blit(timer_text, timer_text_rect)
    
    def _render_player_setup(self, surface: pygame.Surface) -> None:
        """Render player configuration elements."""
        self._render_player_section(surface, 1, 460)
        self._render_player_section(surface, 2, 630)
    
    def _render_player_section(self, surface: pygame.Surface, player_num: int, y_offset: int) -> None:
        """Render setup section for a specific player with background panel."""
        # Semi-transparent panel for player section
        player_panel = pygame.Rect(self.app.WINDOW_WIDTH//2 - 180, y_offset - 10, 360, 160)
        panel_surface = pygame.Surface((player_panel.width, player_panel.height))
        panel_surface.set_alpha(160)
        panel_surface.fill((255, 255, 255))
        surface.blit(panel_surface, player_panel)
        pygame.draw.rect(surface, self.app.BLACK, player_panel, 2)
        
        # Player title (no shadow)
        player_title = self.app.medium_font.render(f"Player {player_num}", True, self.app.NAVY)
        title_rect = player_title.get_rect(center=(self.app.WINDOW_WIDTH//2, y_offset + 10))
        surface.blit(player_title, title_rect)
        
        # Name input with modern styling
        name_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 150, y_offset + 30, 300, 30)
        input_color = self.app.YELLOW if self.app.get_active_input() == f"player{player_num}_name" else self.app.WHITE
        pygame.draw.rect(surface, input_color, name_rect, border_radius=8)
        pygame.draw.rect(surface, self.app.BLACK, name_rect, 2, border_radius=8)
        
        name_text = self.app.medium_font.render(self.app.get_player_name(player_num), True, self.app.BLACK)
        surface.blit(name_text, (name_rect.x + 5, name_rect.y + 5))
        
        # Color selection label (no shadow)
        color_label = self.app.medium_font.render("Color:", True, self.app.NAVY)
        surface.blit(color_label, (self.app.WINDOW_WIDTH//2 - 150, y_offset + 80))
        
        # Color buttons
        self._render_color_buttons(surface, player_num, y_offset + 110)
    
    def _render_color_buttons(self, surface: pygame.Surface, player_num: int, y_pos: int) -> None:
        """Render color selection buttons for a player with modern styling."""
        # Red button
        red_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 100, y_pos, 80, 30)
        red_color = self.app.RED if self.app.get_player_color(player_num) == Color.RED else self.app.LIGHT_RED
        pygame.draw.rect(surface, red_color, red_rect, border_radius=8)
        pygame.draw.rect(surface, self.app.BLACK, red_rect, 2, border_radius=8)
        
        red_text = self.app.small_font.render("RED", True, self.app.WHITE)
        red_text_rect = red_text.get_rect(center=red_rect.center)
        surface.blit(red_text, red_text_rect)
        
        # Blue button
        blue_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 + 20, y_pos, 80, 30)
        blue_color = self.app.BLUE if self.app.get_player_color(player_num) == Color.BLUE else self.app.LIGHT_BLUE
        pygame.draw.rect(surface, blue_color, blue_rect, border_radius=8)
        pygame.draw.rect(surface, self.app.BLACK, blue_rect, 2, border_radius=8)
        
        blue_text = self.app.small_font.render("BLUE", True, self.app.WHITE)
        blue_text_rect = blue_text.get_rect(center=blue_rect.center)
        surface.blit(blue_text, blue_text_rect)
    
    def _render_tutorial_setup(self, surface: pygame.Surface) -> None:
        """Render tutorial mode setup elements with background panel."""
        # Large semi-transparent panel for tutorial info
        tutorial_panel = pygame.Rect(self.app.WINDOW_WIDTH//2 - 340, 350, 700, 400)
        panel_surface = pygame.Surface((tutorial_panel.width, tutorial_panel.height))
        panel_surface.set_alpha(170)
        panel_surface.fill((255, 255, 255))
        surface.blit(panel_surface, tutorial_panel)
        pygame.draw.rect(surface, self.app.BLACK, tutorial_panel, 3)
        
        tutorial_titles = {
            "basic": "Basic Tutorial - Learn the Fundamentals",
            "win": "Win Tutorial - Master the Victory Condition", 
            "lose": "Lose Tutorial - Understand Defeat Scenarios"
        }
        
        # Title (no shadow)
        title_text_content = tutorial_titles.get(self.app.get_tutorial_type(), "Tutorial")
        title_text = self.app.medium_font.render(title_text_content, True, self.app.NAVY)
        title_rect = title_text.get_rect(center=(self.app.WINDOW_WIDTH//2, 380))
        surface.blit(title_text, title_rect)
        
        # Tutorial description (no shadows)
        descriptions = self._get_tutorial_descriptions()
        current_description = descriptions.get(self.app.get_tutorial_type(), [])
        
        y_offset = 290
        for line in current_description:
            if line:  # Skip empty lines
                # Main text only
                line_text = self.app.medium_font.render(line, True, self.app.NAVY)
                line_rect = line_text.get_rect(center=(self.app.WINDOW_WIDTH//2, y_offset + 150))
                surface.blit(line_text, line_rect)
            y_offset += 30
    
    def _get_tutorial_descriptions(self) -> dict:
        """Get tutorial descriptions for each tutorial type."""
        return {
            "basic": [
                "Learn the core mechanics of Santorini!",
                "",
                "In this tutorial you will learn:",
                "• How to select your workers",
                "• How to move around the board", 
                "• How to build structures",
                "• The proper game sequence: Move → Build",
                "",
                "Perfect for first-time players!",
                "Click 'Start Game' when ready!"
            ],
            "win": [
                "",
                "Learn how to win in Santorini!",
                "",
                "In this tutorial you will learn:",
                "• How to position for victory",
                "• How to move to level 3 and win",
                "",
                "Master the winning condition!",
                "Click 'Start Game' when ready!"
            ],
            "lose": [
                "Learn how to avoid defeat in Santorini!",
                "",
                "In this tutorial you will experience:",
                "• Getting trapped by buildings",
                "• When you can't move any worker",
                "• How positioning affects survival",
                "",
                "Understand the losing condition!",
                "Click 'Start Game' when ready!"
            ]
        }
    
    def _render_start_button(self, surface: pygame.Surface) -> None:
        """Render the start game button with modern styling."""
        start_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 100, 800, 200, 50)
        
        # Button shadow
        shadow_rect = pygame.Rect(start_rect.x + 3, start_rect.y + 3, start_rect.width, start_rect.height)
        pygame.draw.rect(surface, self.app.SHADOW, shadow_rect, border_radius=15)
        
        # Main button
        pygame.draw.rect(surface, self.app.EMERALD, start_rect, border_radius=15)
        pygame.draw.rect(surface, self.app.BLACK, start_rect, 3, border_radius=15)
        
        # Button text (no shadow)
        start_text = self.app.medium_font.render("Start Game", True, self.app.WHITE)
        start_text_rect = start_text.get_rect(center=start_rect.center)
        surface.blit(start_text, start_text_rect)
    
    def _start_game(self) -> None:
        """Start the game with current settings."""
        if self.app.get_game_mode_type() == "tutorial":
            self._start_tutorial_game()
        else:
            self._start_standard_game()
    
    def _start_tutorial_game(self) -> None:
        """Start a tutorial game."""
        # Create single player for tutorial (no timer needed)
        player = Player("Tutorial Player", 0, Color.BLUE, timer_seconds=None)
        game_mode = TutorialGameMode(self.app.get_tutorial_type())
        
        # Register as observer for tutorial events
        game_mode.tutorial_manager.add_observer(self.app.get_tutorial_adapter())
        
        # Create game with tutorial mode
        game = Game([player], self.app.BOARD_W, self.app.BOARD_H, game_mode=game_mode)
        self.app.set_game(game)
        
        # Initialize tutorial UI
        self.app.update_tutorial_ui()
        
        # Switch to game screen
        self.app.change_screen(ScreenType.GAME)
    
    def _start_standard_game(self) -> None:
        """Start a standard game."""
        # Validate inputs
        if not self._validate_standard_inputs():
            return
        
        # Create players
        timer_seconds = self.app.get_timer_minutes() * 60
        player1 = Player(
            self.app.get_player_name(1).strip(), 
            0, 
            self.app.get_player_color(1), 
            timer_seconds=timer_seconds
        )
        player2 = Player(
            self.app.get_player_name(2).strip(), 
            0, 
            self.app.get_player_color(2), 
            timer_seconds=timer_seconds
        )
        
        # Create game
        game_mode = StandardGameMode()
        game = Game([player1, player2], self.app.BOARD_W, self.app.BOARD_H, game_mode=game_mode)
        self.app.set_game(game)
        
        # Switch to game screen
        self.app.change_screen(ScreenType.GAME)
    
    def _validate_standard_inputs(self) -> bool:
        """Validate inputs for standard game mode."""
        if not self.app.get_player_name(1).strip():
            self.app.show_message("Player 1 must enter a name!")
            return False
        if not self.app.get_player_name(2).strip():
            self.app.show_message("Player 2 must enter a name!")
            return False
        if not self.app.get_player_color(1):
            self.app.show_message("Player 1 must select a color!")
            return False
        if not self.app.get_player_color(2):
            self.app.show_message("Player 2 must select a color!")
            return False
        if self.app.get_player_color(1) == self.app.get_player_color(2):
            self.app.show_message("Players must choose different colors!")
            return False
        return True 