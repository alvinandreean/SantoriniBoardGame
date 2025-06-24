from typing import Tuple
import pygame
from ui.base_screen import BaseScreen
from ui.screen_enums import ScreenType
from utils.resource_manager import ResourceManager


class GameOverScreen(BaseScreen):
    """Game over screen showing the winner and options to play again or return to menu."""
    
    def __init__(self, app):
        """Initialize the game over screen"""
        super().__init__(app)
        self.hover_button = None  # Track which button is being hovered
        self.background_image = None
        self.winner_text = ""
        self.game_mode = ""
        self._load_assets()
    
    def _load_assets(self):
        """Load background image and other assets."""
        self.background_image = ResourceManager.load_image("assets/game.png")
        
        # Scale background to fit window
        if self.background_image:
            self.background_image = pygame.transform.scale(
                self.background_image, 
                (self.app.WINDOW_WIDTH, self.app.WINDOW_HEIGHT)
            )
    
    def set_game_result(self, winner_text: str, game_mode: str = "standard"):
        """Set the game result information to display."""
        self.winner_text = winner_text
        self.game_mode = game_mode
    
    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle clicks on game over screen buttons."""
        x, y = pos
        
        # Play Again button
        play_again_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 250, 500, 200, 70)
        if play_again_rect.collidepoint(x, y):
            if self.game_mode == "tutorial":
                self.app.change_screen(ScreenType.TUTORIAL_SELECTION)
            else:
                self.app.change_screen(ScreenType.SETUP)
            return
        
        # Main Menu button
        main_menu_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 + 50, 500, 200, 70)
        if main_menu_rect.collidepoint(x, y):
            self.app.change_screen(ScreenType.MAIN_MENU)
            return
    
    def handle_keypress(self, event: pygame.event.Event) -> None:
        """Handle keyboard input."""
        if event.key == pygame.K_ESCAPE:
            self.app.change_screen(ScreenType.MAIN_MENU)
        elif event.key == pygame.K_SPACE:
            # Space to play again
            if self.game_mode == "tutorial":
                self.app.change_screen(ScreenType.TUTORIAL_SELECTION)
            else:
                self.app.change_screen(ScreenType.SETUP)
    
    def update(self) -> None:
        """Update hover states based on mouse position."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Check which button is being hovered
        play_again_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 250, 500, 200, 70)
        main_menu_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 + 50, 500, 200, 70)
        
        if play_again_rect.collidepoint(mouse_pos):
            self.hover_button = "play_again"
        elif main_menu_rect.collidepoint(mouse_pos):
            self.hover_button = "main_menu"
        else:
            self.hover_button = None
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the game over screen."""
        self._render_background(surface)
        self._render_victory_panel(surface)
        self._render_buttons(surface)
        self._render_instructions(surface)
    
    def _render_background(self, surface: pygame.Surface) -> None:
        """Render the background with overlay."""
        if self.background_image:
            # Use the game background image
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill(self.app.NAVY)
        
        overlay = pygame.Surface((self.app.WINDOW_WIDTH, self.app.WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
    
    def _render_victory_panel(self, surface: pygame.Surface) -> None:
        """Render the victory announcement panel."""

        panel_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 400, 200, 800, 200)
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height))
        panel_surface.set_alpha(220)
        panel_surface.fill(self.app.WHITE)
        surface.blit(panel_surface, panel_rect)
        pygame.draw.rect(surface, self.app.GOLD, panel_rect, 4, border_radius=20)
        
        # Game Over title
        game_over_text = self.app.title_font.render("GAME OVER", True, self.app.NAVY)
        game_over_rect = game_over_text.get_rect(center=(panel_rect.centerx, panel_rect.y + 60))
        surface.blit(game_over_text, game_over_rect)
        
        # Winner text
        winner_color = self.app.EMERALD if "wins" in self.winner_text else self.app.CORAL
        winner_surface = self.app.large_font.render(self.winner_text, True, winner_color)
        winner_rect = winner_surface.get_rect(center=(panel_rect.centerx, panel_rect.y + 140))
        surface.blit(winner_surface, winner_rect)
    
    def _render_buttons(self, surface: pygame.Surface) -> None:
        """Render the action buttons."""
        # Play Again button
        play_again_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 250, 500, 200, 70)
        play_again_text = "Play Again" if self.game_mode != "tutorial" else "Try Again"
        self._render_modern_button(surface, play_again_text, play_again_rect, self.app.EMERALD, "play_again")
        
        # Main Menu button
        main_menu_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 + 50, 500, 200, 70)
        self._render_modern_button(surface, "Main Menu", main_menu_rect, self.app.CORAL, "main_menu")
    
    def _render_instructions(self, surface: pygame.Surface) -> None:
        """Render keyboard instructions."""
        instructions = [
            "Press SPACE to play again",
            "Press ESC for main menu"
        ]
        
        y_offset = 620
        for instruction in instructions:
            instruction_text = self.app.medium_font.render(instruction, True, self.app.WHITE)
            instruction_rect = instruction_text.get_rect(center=(self.app.WINDOW_WIDTH//2, y_offset))
            
            shadow_text = self.app.medium_font.render(instruction, True, self.app.BLACK)
            shadow_rect = shadow_text.get_rect(center=(self.app.WINDOW_WIDTH//2 + 2, y_offset + 2))
            surface.blit(shadow_text, shadow_rect)
            surface.blit(instruction_text, instruction_rect)
            
            y_offset += 35
    
    def _render_modern_button(self, surface: pygame.Surface, text: str, rect: pygame.Rect, color: tuple, button_id: str) -> None:
        """Render a single button with modern styling and hover effects."""
        # Determine if this button is hovered
        is_hovered = self.hover_button == button_id
        
        # Base color (lighter when hovered)
        button_color = tuple(min(255, c + 30) for c in color) if is_hovered else color

        shadow_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width, rect.height)
        pygame.draw.rect(surface, self.app.SHADOW, shadow_rect, border_radius=15)
        
        # Draw main button with rounded corners
        pygame.draw.rect(surface, button_color, rect, border_radius=15)
        
        # Draw border
        border_color = self.app.WHITE if is_hovered else self.app.SHADOW
        pygame.draw.rect(surface, border_color, rect, width=3, border_radius=15)
        
        # Draw text
        text_color = self.app.WHITE if not is_hovered else self.app.SHADOW
        button_text = self.app.large_font.render(text, True, text_color)
        text_rect = button_text.get_rect(center=rect.center)
        surface.blit(button_text, text_rect) 