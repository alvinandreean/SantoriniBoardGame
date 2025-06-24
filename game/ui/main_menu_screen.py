from typing import Tuple
import pygame
from ui.base_screen import BaseScreen
from ui.screen_enums import ScreenType
from utils.resource_manager import ResourceManager


class MainMenuScreen(BaseScreen):
    """Main menu screen with title and navigation buttons."""
    
    def __init__(self, app):
        """Initialize the main menu screen."""
        super().__init__(app)
        self.hover_button = None  # Track which button is being hovered
        self.background_image = None
        self.title_image = None
        self._load_assets()
    
    def _load_assets(self):
        """Load background image, title image and other assets."""
        self.background_image = ResourceManager.load_image("assets/background.png")
        self.title_image = ResourceManager.load_image("assets/title.png")

        if self.background_image:
            self.background_image = pygame.transform.scale(
                self.background_image, 
                (self.app.WINDOW_WIDTH, self.app.WINDOW_HEIGHT)
            )
        
        if self.title_image:
            title_width = min(800, self.app.WINDOW_WIDTH - 50)  
            original_width, original_height = self.title_image.get_size()
            aspect_ratio = original_height / original_width
            title_height = int(title_width * aspect_ratio)
            self.title_image = pygame.transform.scale(self.title_image, (title_width, title_height))
    
    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle clicks on main menu buttons."""
        x, y = pos
        
        # Start New Game button
        start_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 450, 400, 70)
        if start_rect.collidepoint(x, y):
            self.app.change_screen(ScreenType.SETUP)
            return
            
        # Tutorial button
        tutorial_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 550, 400, 70)
        if tutorial_rect.collidepoint(x, y):
            self.app.change_screen(ScreenType.TUTORIAL_SELECTION)
            return
        
        # Exit button
        exit_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 650, 400, 70)
        if exit_rect.collidepoint(x, y):
            self.app.quit_application()
    
    def handle_keypress(self, event: pygame.event.Event) -> None:
        """Main menu doesn't handle keyboard input."""
        pass
    
    def update(self) -> None:
        """Update hover states based on mouse position."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Check which button is being hovered
        start_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 450, 400, 70)
        tutorial_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 550, 400, 70)
        exit_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 650, 400, 70)
        
        if start_rect.collidepoint(mouse_pos):
            self.hover_button = "start"
        elif tutorial_rect.collidepoint(mouse_pos):
            self.hover_button = "tutorial"
        elif exit_rect.collidepoint(mouse_pos):
            self.hover_button = "exit"
        else:
            self.hover_button = None
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the beautiful main menu."""
        self._render_background(surface)
        self._render_title(surface)
        self._render_buttons(surface)
    
    def _render_background(self, surface: pygame.Surface) -> None:
        """Render the background image or fallback gradient."""
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
        else:
            for y in range(self.app.WINDOW_HEIGHT):
                blend_ratio = y / self.app.WINDOW_HEIGHT
                r = int(self.app.OCEAN_BLUE[0] * (1 - blend_ratio) + self.app.CREAM[0] * blend_ratio)
                g = int(self.app.OCEAN_BLUE[1] * (1 - blend_ratio) + self.app.CREAM[1] * blend_ratio)
                b = int(self.app.OCEAN_BLUE[2] * (1 - blend_ratio) + self.app.CREAM[2] * blend_ratio)
                pygame.draw.line(surface, (r, g, b), (0, y), (self.app.WINDOW_WIDTH, y))
    
    def _render_title(self, surface: pygame.Surface) -> None:
        """Render the game title using title.png image."""
        if self.title_image:
            # Center the title image
            title_rect = self.title_image.get_rect(center=(self.app.WINDOW_WIDTH//2, 250))
            surface.blit(self.title_image, title_rect)
        else:
            shadow_text = self.app.title_font.render("Santorini", True, self.app.BLACK)
            shadow_rect = shadow_text.get_rect(center=(self.app.WINDOW_WIDTH//2 + 4, 250 + 4))
            surface.blit(shadow_text, shadow_rect)
            
            # Main title with gold color
            title_text = self.app.title_font.render("Santorini", True, self.app.GOLD)
            title_rect = title_text.get_rect(center=(self.app.WINDOW_WIDTH//2, 250))
            surface.blit(title_text, title_rect)
    
    def _render_buttons(self, surface: pygame.Surface) -> None:
        """Render all menu buttons with modern styling."""
        self._render_modern_button(surface, "Start New Game", 
                                  pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 450, 400, 70),
                                  self.app.EMERALD, "start")
        
        self._render_modern_button(surface, "Tutorial", 
                                  pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 550, 400, 70),
                                  self.app.LAVENDER, "tutorial")
        
        self._render_modern_button(surface, "Exit", 
                                  pygame.Rect(self.app.WINDOW_WIDTH//2 - 200, 650, 400, 70),
                                  self.app.CORAL, "exit")
    
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
        
        text_color = self.app.WHITE if not is_hovered else self.app.SHADOW
        button_text = self.app.large_font.render(text, True, text_color)
        text_rect = button_text.get_rect(center=rect.center)
        surface.blit(button_text, text_rect) 