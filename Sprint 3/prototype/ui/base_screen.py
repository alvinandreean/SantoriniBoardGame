from abc import ABC, abstractmethod
from typing import Tuple
import pygame


class BaseScreen(ABC):
    """Abstract base class for all game screens following OOP principles."""
    
    def __init__(self, app):
        """Initialize with reference to main app for accessing shared resources."""
        self.app = app
        
    @abstractmethod
    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle mouse clicks on this screen."""
        pass
        
    @abstractmethod
    def handle_keypress(self, event: pygame.event.Event) -> None:
        """Handle keyboard input on this screen."""
        pass
        
    @abstractmethod
    def update(self) -> None:
        """Update screen state each frame."""
        pass
        
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Render this screen to the given surface."""
        pass
        
    def on_enter(self) -> None:
        """Called when entering this screen. Override if needed."""
        pass
        
    def on_exit(self) -> None:
        """Called when leaving this screen. Override if needed."""
        pass 