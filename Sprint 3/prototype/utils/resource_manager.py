import pygame
import sys
import os
from typing import Optional

class ResourceManager:
    """Manages resource loading for both development and PyInstaller executable"""
    
    _background_music_playing = False
    
    @staticmethod
    def get_asset_path(relative_path: str) -> str:
        """Get absolute path to resource"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            # If not an executable, use current directory
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
    
    @staticmethod
    def load_image(image_path: str) -> pygame.Surface:
        """Load an image from the assets folder."""
        full_path = ResourceManager.get_asset_path(image_path)
        try:
            return pygame.image.load(full_path)
        except pygame.error as e:
            print(f"Could not load image {image_path}: {e}")
            surface = pygame.Surface((100, 100))
            surface.fill((255, 0, 255)) 
            return surface
    
    @staticmethod
    def load_sound(sound_path: str) -> Optional[pygame.mixer.Sound]:
        """Load a sound from the assets folder."""
        full_path = ResourceManager.get_asset_path(sound_path)
        try:
            return pygame.mixer.Sound(full_path)
        except pygame.error as e:
            print(f"Could not load sound {sound_path}: {e}")
            return None
    
    @staticmethod
    def load_and_play_background_music(music_path: str, volume: float = 0.5, loops: int = -1) -> None:
        """Load and play background music."""
        if not ResourceManager._background_music_playing:
            full_path = ResourceManager.get_asset_path(music_path)
            try:
                pygame.mixer.music.load(full_path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loops)
                ResourceManager._background_music_playing = True
                print(f"Background music started: {music_path}")
            except pygame.error as e:
                print(f"Could not load/play music {music_path}: {e}")
    
    @staticmethod
    def stop_background_music() -> None:
        """Stop background music."""
        pygame.mixer.music.stop()
        ResourceManager._background_music_playing = False
    
    @staticmethod
    def set_music_volume(volume: float) -> None:
        """Set background music volume (0.0 to 1.0)."""
        pygame.mixer.music.set_volume(volume) 