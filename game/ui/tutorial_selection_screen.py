from typing import Tuple
import pygame
from ui.base_screen import BaseScreen
from ui.screen_enums import ScreenType
from utils.resource_manager import ResourceManager


class TutorialSelectionScreen(BaseScreen):
    """Tutorial selection screen with different tutorial options."""
    
    def __init__(self, app):
        """Initialize the tutorial selection screen."""
        super().__init__(app)
        self.hover_button = None  # Track which button is being hovered
        self.background_image = None
        self._load_assets()
    
    def _load_assets(self):
        """Load background image and other assets."""
        self.background_image = ResourceManager.load_image("assets/tutor.png")
        
        if self.background_image:
            self.background_image = pygame.transform.scale(
                self.background_image, 
                (self.app.WINDOW_WIDTH, self.app.WINDOW_HEIGHT)
            )
    
    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle clicks on tutorial selection buttons."""
        x, y = pos
        
        # Basic Tutorial button
        basic_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 350, 400, 70)
        if basic_rect.collidepoint(x, y):
            self.app.set_tutorial_mode("basic")
            self.app.change_screen(ScreenType.SETUP)
            return
        
        # Win Tutorial button
        win_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 450, 400, 70)
        if win_rect.collidepoint(x, y):
            self.app.set_tutorial_mode("win")
            self.app.change_screen(ScreenType.SETUP)
            return
        
        # Lose Tutorial button
        lose_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 550, 400, 70)
        if lose_rect.collidepoint(x, y):
            self.app.set_tutorial_mode("lose")
            self.app.change_screen(ScreenType.SETUP)
            return
        
        # Back button
        back_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 150, 670, 300, 60)
        if back_rect.collidepoint(x, y):
            self.app.change_screen(ScreenType.MAIN_MENU)
    
    def handle_keypress(self, event: pygame.event.Event) -> None:
        """Tutorial selection doesn't handle keyboard input."""
        pass
    
    def update(self) -> None:
        """Update hover states based on mouse position."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Check which button is being hovered
        basic_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 350, 400, 70)
        win_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 450, 400, 70)
        lose_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 550, 400, 70)
        back_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 150, 670, 300, 60)
        
        if basic_rect.collidepoint(mouse_pos):
            self.hover_button = "basic"
        elif win_rect.collidepoint(mouse_pos):
            self.hover_button = "win"
        elif lose_rect.collidepoint(mouse_pos):
            self.hover_button = "lose"
        elif back_rect.collidepoint(mouse_pos):
            self.hover_button = "back"
        else:
            self.hover_button = None
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the tutorial selection screen."""
        self._render_background(surface)
        self._render_title(surface)
        self._render_tutorial_buttons(surface)
        self._render_back_button(surface)
    
    def _render_background(self, surface: pygame.Surface) -> None:
        """Render the background image or fallback to solid color."""
        if self.background_image:
            # Use the loaded tutor background image
            surface.blit(self.background_image, (0, 0))
        else:
            for y in range(self.app.WINDOW_HEIGHT):
                blend_ratio = y / self.app.WINDOW_HEIGHT
                r = int(self.app.LAVENDER[0] * (1 - blend_ratio) + self.app.CREAM[0] * blend_ratio)
                g = int(self.app.LAVENDER[1] * (1 - blend_ratio) + self.app.CREAM[1] * blend_ratio)
                b = int(self.app.LAVENDER[2] * (1 - blend_ratio) + self.app.CREAM[2] * blend_ratio)
                pygame.draw.line(surface, (r, g, b), (0, y), (self.app.WINDOW_WIDTH, y))
    
    def _render_title(self, surface: pygame.Surface) -> None:
        """Render the screen title with shadow for visibility."""
        shadow_text = self.app.title_font.render("Tutorial Selection", True, self.app.BLACK)
        shadow_rect = shadow_text.get_rect(center=(self.app.WINDOW_WIDTH//2 + 4, 200 + 4))
        surface.blit(shadow_text, shadow_rect)
        
        # Main title with gold color
        title_text = self.app.title_font.render("Tutorial Selection", True, self.app.GOLD)
        title_rect = title_text.get_rect(center=(self.app.WINDOW_WIDTH//2, 200))
        surface.blit(title_text, title_rect)
    
    def _render_tutorial_buttons(self, surface: pygame.Surface) -> None:
        """Render tutorial type selection buttons with modern styling."""
        self._render_modern_button(surface, "Basic Tutorial", 
                          pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 350, 400, 70),
                          self.app.EMERALD, "basic")
        
        self._render_modern_button(surface, "Win Tutorial", 
                          pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 450, 400, 70),
                          self.app.OCEAN_BLUE, "win")
        
        self._render_modern_button(surface, "Lose Tutorial", 
                          pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 550, 400, 70),
                          self.app.SUNSET_ORANGE, "lose")
    
    def _render_back_button(self, surface: pygame.Surface) -> None:
        """Render the back button with modern styling."""
        back_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 150, 670, 300, 60)
        self._render_modern_button(surface, "Back", back_rect, self.app.CORAL, "back")
    
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
        
        border_color = self.app.WHITE if is_hovered else self.app.SHADOW
        pygame.draw.rect(surface, border_color, rect, width=3, border_radius=15)
        
        # Draw text
        text_color = self.app.WHITE if not is_hovered else self.app.SHADOW
        button_text = self.app.large_font.render(text, True, text_color)
        text_rect = button_text.get_rect(center=rect.center)
        surface.blit(button_text, text_rect) 