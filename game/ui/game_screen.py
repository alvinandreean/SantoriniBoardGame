from typing import Tuple
import pygame
from ui.base_screen import BaseScreen
from ui.screen_enums import ScreenType
from core.position import Position
from utils.resource_manager import ResourceManager


class GameScreen(BaseScreen):
    """Game screen for playing Santorini with board visualization and controls."""
    
    def __init__(self, app):
        """Initialize the game screen"""
        super().__init__(app)
        self.red_worker_image = None
        self.blue_worker_image = None
        self.background_image = None
        self.grass_tile_image = None
        self.grass_dark_tile_image = None
        self.god_card_images = {}  
        self._load_assets()
    
    def _load_assets(self):
        """Load worker images, background image, tile images, god card images and other assets."""
        self.red_worker_image = ResourceManager.load_image("assets/red_worker.png")
        self.blue_worker_image = ResourceManager.load_image("assets/blue_worker.png")
        self.background_image = ResourceManager.load_image("assets/game.png")
        self.grass_tile_image = ResourceManager.load_image("assets/grass.png")
        self.grass_dark_tile_image = ResourceManager.load_image("assets/grass_dark.png")
        
        # Load god card images
        god_names = ["artemis", "demeter", "triton"]
        for god_name in god_names:
            god_image = ResourceManager.load_image(f"assets/{god_name}.png")
            if god_image:
                self.god_card_images[god_name] = pygame.transform.smoothscale(god_image, (280, 380))
        
        if self.red_worker_image:
            self.red_worker_image = pygame.transform.scale(self.red_worker_image, (36, 36))
        if self.blue_worker_image:
            self.blue_worker_image = pygame.transform.scale(self.blue_worker_image, (36, 36))

        if self.background_image:
            self.background_image = pygame.transform.scale(
                self.background_image, 
                (self.app.WINDOW_WIDTH, self.app.WINDOW_HEIGHT)
            )
        
        if self.grass_tile_image:
            tile_image_size = int(self.app.TILE_SIZE * 1.1) 
            self.grass_tile_image = pygame.transform.scale(
                self.grass_tile_image, 
                (tile_image_size, tile_image_size)
            )
        if self.grass_dark_tile_image:
            tile_image_width = int(self.app.TILE_SIZE * 1.1)
            tile_image_height = int(self.app.TILE_SIZE * 1.15)  
            self.grass_dark_tile_image = pygame.transform.scale(
                self.grass_dark_tile_image, 
                (tile_image_width, tile_image_height)
            )
    
    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle clicks during gameplay."""
        x, y = pos
        
        if self._handle_ui_button_clicks(pos):
            return
        
        # Handle board clicks
        self._handle_board_click(pos)
    
    def _handle_ui_button_clicks(self, pos: Tuple[int, int]) -> bool:
        """Handle clicks on UI buttons. Returns True if a button was clicked."""
        
        # Main Menu button
        menu_rect = pygame.Rect(50, 50, 120, 40)
        if menu_rect.collidepoint(pos):
            self.app.change_screen(ScreenType.MAIN_MENU)
            return True
        
        # Skip button - always shown on bottom left
        game = self.app.get_game()
        skip_rect = pygame.Rect(50, self.app.WINDOW_HEIGHT - 60, 120, 50)
        if skip_rect.collidepoint(pos) and game and game.current_phase_optional():
            game.skip_phase()
            return True
        
        # Quit Game button - bottom right
        quit_rect = pygame.Rect(self.app.WINDOW_WIDTH - 170, self.app.WINDOW_HEIGHT - 60, 120, 50)
        if quit_rect.collidepoint(pos):
            self.app.change_screen(ScreenType.MAIN_MENU)
            return True
        
        # Tutorial specific buttons
        if self.app.is_tutorial_mode():
            return self._handle_tutorial_buttons(pos)
        
        return False
    
    def _handle_tutorial_buttons(self, pos: Tuple[int, int]) -> bool:
        """Handle tutorial-specific button clicks."""
        return False
    
    def _handle_board_click(self, pos: Tuple[int, int]) -> None:
        """Handle clicks on the game board."""
        board_x, board_y = self._screen_to_board_coords(pos)
        
        if board_x is not None and board_y is not None:
            self._process_board_click(board_x, board_y)
    
    def _screen_to_board_coords(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Convert screen coordinates to board coordinates."""
        x, y = pos
        
        board_offset_x = int(0.3 * self.app.WINDOW_WIDTH - (self.app.BOARD_W * self.app.TILE_SIZE) // 2)
        board_offset_y = (self.app.WINDOW_HEIGHT - (self.app.BOARD_H * self.app.TILE_SIZE)) // 2
        
        # Check if click is within board area
        if (x < board_offset_x or x >= board_offset_x + (self.app.BOARD_W * self.app.TILE_SIZE) or
            y < board_offset_y or y >= board_offset_y + (self.app.BOARD_H * self.app.TILE_SIZE)):
            return None, None
        
        # Convert to board coordinates
        board_x = (x - board_offset_x) // self.app.TILE_SIZE
        board_y = (y - board_offset_y) // self.app.TILE_SIZE
        
        return board_x, board_y
    
    def _process_board_click(self, board_x: int, board_y: int) -> None:
        """Process a click on the game board."""
        game = self.app.get_game()
        if not game:
            return
        
        feedback = game.click_cell(board_x, board_y)
        
        if feedback:
            self.app.show_message(feedback)
        
        # Update tutorial UI if in tutorial mode
        if self.app.is_tutorial_mode():
            self.app.update_tutorial_ui()
        else:
            # Check for game result after the move in standard mode
            game_result = game.turn_manager.get_game_result()
            if game_result:
                self.app.handle_game_over(f"{game_result.player_name} wins!")
    
    def handle_keypress(self, event: pygame.event.Event) -> None:
        """Handle keyboard input during gameplay."""
        if event.key == pygame.K_ESCAPE:
            self.app.change_screen(ScreenType.MAIN_MENU)
    
    def update(self) -> None:
        """Update game state each frame."""
        game = self.app.get_game()
        if game and not self.app.is_tutorial_mode():
            self._check_timer_expiration()
    
    def _check_timer_expiration(self) -> None:
        """Check for timer expiration in standard games."""
        game = self.app.get_game()
        current_player = game.turn_manager.current_player
        
        if current_player.get_remaining_time() <= 0:
            # Time expired - other player wins
            # Get current player index from the sequence
            current_index = game.turn_manager._players.index
            other_index = (current_index + 1) % len(game.players)
            other_player = game.players[other_index]
            self.app.handle_game_over(f"{other_player.player_name} wins by timeout!")
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the game screen."""
        self._render_background(surface)
        self._render_current_player_panel(surface)
        self._render_ui_buttons(surface)
        self._render_game_board(surface)
        self._render_game_info(surface)
        self._render_god_cards(surface)
        
        # Render mode-specific elements
        if self.app.is_tutorial_mode():
            self._render_tutorial_elements(surface)
        else:
            self._render_standard_game_elements(surface)
    
    def _render_background(self, surface: pygame.Surface) -> None:
        """Render the background image or fallback to solid color."""
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill(self.app.WHITE)
    
    def _render_current_player_panel(self, surface: pygame.Surface) -> None:
        """Render current player info in transparent panel at top center."""
        game = self.app.get_game()
        if not game:
            return
        
        current_player = game.turn_manager.current_player
        
        panel_rect = pygame.Rect(self.app.WINDOW_WIDTH//2 - 150, 30, 300, 60)
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height))
        panel_surface.set_alpha(180)  # Semi-transparent
        panel_surface.fill((255, 255, 255))  # White background
        surface.blit(panel_surface, panel_rect)
        pygame.draw.rect(surface, self.app.BLACK, panel_rect, 2, border_radius=10)
        
        # Current player text
        player_text = f"Current Turn: {current_player.player_name}"
        player_surface = self.app.medium_font.render(player_text, True, self.app.BLACK)
        text_rect = player_surface.get_rect(center=panel_rect.center)
        surface.blit(player_surface, text_rect)
    
    def _render_ui_buttons(self, surface: pygame.Surface) -> None:
        """Render the UI control buttons."""
        # Main Menu button
        menu_rect = pygame.Rect(50, 50, 120, 40)
        pygame.draw.rect(surface, self.app.LIGHT_GRAY, menu_rect)
        pygame.draw.rect(surface, self.app.BLACK, menu_rect, 2)
        
        menu_text = self.app.medium_font.render("Main Menu", True, self.app.BLACK)
        menu_text_rect = menu_text.get_rect(center=menu_rect.center)
        surface.blit(menu_text, menu_text_rect)
        
        # Skip button - always shown on bottom left (greyed out if not optional action)
        game = self.app.get_game()
        skip_rect = pygame.Rect(50, self.app.WINDOW_HEIGHT - 60, 120, 50)
        
        is_optional = game and game.current_phase_optional()
        skip_color = self.app.YELLOW if is_optional else self.app.GRAY
        text_color = self.app.BLACK if is_optional else self.app.DARK_GRAY
        
        pygame.draw.rect(surface, skip_color, skip_rect)
        pygame.draw.rect(surface, self.app.BLACK, skip_rect, 2)
        
        skip_text = self.app.medium_font.render("Skip", True, text_color)
        skip_text_rect = skip_text.get_rect(center=skip_rect.center)
        surface.blit(skip_text, skip_text_rect)
        
        # Quit Game button - bottom right
        quit_rect = pygame.Rect(self.app.WINDOW_WIDTH - 170, self.app.WINDOW_HEIGHT - 60, 120, 50)
        pygame.draw.rect(surface, self.app.CORAL, quit_rect)
        pygame.draw.rect(surface, self.app.BLACK, quit_rect, 2)
        
        quit_text = self.app.medium_font.render("Quit Game", True, self.app.WHITE)
        quit_text_rect = quit_text.get_rect(center=quit_rect.center)
        surface.blit(quit_text, quit_text_rect)
    
    def _render_game_board(self, surface: pygame.Surface) -> None:
        """Render the Santorini game board."""
        game = self.app.get_game()
        if not game:
            return
        
        board = game.board
        board_offset_x = int(0.3 * self.app.WINDOW_WIDTH - (self.app.BOARD_W * self.app.TILE_SIZE) // 2)
        board_offset_y = (self.app.WINDOW_HEIGHT - (self.app.BOARD_H * self.app.TILE_SIZE)) // 2
        
        for y in range(self.app.BOARD_H):
            for x in range(self.app.BOARD_W):
                tile_x = board_offset_x + x * self.app.TILE_SIZE
                tile_y = board_offset_y + y * self.app.TILE_SIZE
                
                self._render_tile(surface, board, x, y, tile_x, tile_y)
    
    def _render_tile(self, surface: pygame.Surface, board, x: int, y: int, tile_x: int, tile_y: int) -> None:
        """Render a single tile on the game board using grass images."""
        tile = board.get_tile(Position(x, y))
        tile_rect = pygame.Rect(tile_x, tile_y, self.app.TILE_SIZE, self.app.TILE_SIZE)
        
        # Tile background using grass images in alternating pattern
        is_light_tile = (x + y) % 2 == 0  # Checkerboard pattern
        
        if is_light_tile and self.grass_tile_image:
            # Light grass tile - center the larger image
            image_offset = int((self.grass_tile_image.get_width() - self.app.TILE_SIZE) / 2)
            surface.blit(self.grass_tile_image, (tile_x - image_offset, tile_y - image_offset))
        elif not is_light_tile and self.grass_dark_tile_image:
            # Dark grass tile - center the larger image
            image_offset = int((self.grass_dark_tile_image.get_width() - self.app.TILE_SIZE) / 2)
            surface.blit(self.grass_dark_tile_image, (tile_x - image_offset, tile_y - image_offset))
        else:
            tile_color = self.app.LIGHT_GRAY if is_light_tile else self.app.GRAY
            pygame.draw.rect(surface, tile_color, tile_rect)
        
        # Tile border
        pygame.draw.rect(surface, self.app.BLACK, tile_rect, 2)
        
        # Building levels
        self._render_building(surface, tile, tile_x, tile_y)
        
        # Worker
        if tile.worker:
            self._render_worker(surface, tile.worker, tile_x, tile_y)
        
        # Tile highlighting
        self._render_tile_highlighting(surface, x, y, tile_rect)
    
    def _render_building(self, surface: pygame.Surface, tile, tile_x: int, tile_y: int) -> None:
        """Render building levels on a tile with white outlines and blue dome."""
        # Check if tile has a building before accessing properties
        if tile.building is None:
            return
            
        building_height = tile.building.level
        
        if building_height == 0:
            return
        
        # Draw multiple transparent squares, getting smaller for each level
        for level in range(building_height):
            # Calculate size - smaller for higher levels
            margin = 10 + (level * 8)  # Each level adds more margin (gets smaller)
            
            if level < 3:  # Levels 1-3 are squares
                building_rect = pygame.Rect(
                    tile_x + margin, 
                    tile_y + margin,
                    self.app.TILE_SIZE - (margin * 2), 
                    self.app.TILE_SIZE - (margin * 2)
                )
                
                # Draw white outline instead of black
                pygame.draw.rect(surface, self.app.WHITE, building_rect, 2)
            else:  # Level 4 (dome) is a circle
                # Circle should be smaller than level 3 square
                center_x = tile_x + self.app.TILE_SIZE // 2
                center_y = tile_y + self.app.TILE_SIZE // 2
                radius = (self.app.TILE_SIZE - (margin * 2)) // 3  # Smaller than square
                
                # Draw filled blue circle for dome
                pygame.draw.circle(surface, self.app.BLUE, (center_x, center_y), radius)
    
    def _render_worker(self, surface: pygame.Surface, worker, tile_x: int, tile_y: int) -> None:
        """Render worker using PNG image with color tinting."""
        center_x = tile_x + self.app.TILE_SIZE // 2
        center_y = tile_y + self.app.TILE_SIZE // 2
        
        if worker.color.name == "RED":
            worker_image = self.red_worker_image
        else:  # BLUE
            worker_image = self.blue_worker_image
        
        if worker_image:
            # Calculate position to center the image
            image_rect = worker_image.get_rect()
            image_rect.center = (center_x, center_y)
            
            shadow_offset = 3
            shadow_rect = image_rect.copy()
            shadow_rect.x += shadow_offset
            shadow_rect.y += shadow_offset
            
            shadow_surface = worker_image.copy()
            shadow_surface.fill((0, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(shadow_surface, shadow_rect)
            
            # Draw the main worker image
            surface.blit(worker_image, image_rect)
        else:
            self._render_worker_fallback(surface, worker, center_x, center_y)
    
    def _render_worker_fallback(self, surface: pygame.Surface, worker, center_x: int, center_y: int) -> None:
        """Fallback worker rendering using circles if image fails."""
        # Worker colors
        if worker.color.name == "RED":
            worker_color = self.app.RED
            highlight_color = self.app.LIGHT_RED
        else:  # BLUE
            worker_color = self.app.BLUE
            highlight_color = self.app.LIGHT_BLUE
        
        shadow_center = (center_x + 2, center_y + 2)
        pygame.draw.circle(surface, self.app.SHADOW, shadow_center, 18)
        
        # Worker main body
        pygame.draw.circle(surface, worker_color, (center_x, center_y), 18)
        
        # Worker highlight
        pygame.draw.circle(surface, highlight_color, (center_x - 4, center_y - 4), 8)
        
        # Worker border
        pygame.draw.circle(surface, self.app.WHITE, (center_x, center_y), 18, width=2)
        
        # Worker center dot
        pygame.draw.circle(surface, self.app.WHITE, (center_x, center_y), 4)
    
    def _render_tile_highlighting(self, surface: pygame.Surface, x: int, y: int, 
                                 tile_rect: pygame.Rect) -> None:
        """Render highlighting for selected tiles and valid moves with semi-transparent fill."""
        game = self.app.get_game()
        if not game:
            return
        
        # Highlight selected worker position with semi-transparent yellow
        selected_pos = game.selected_worker_pos()
        if selected_pos and selected_pos == (x, y):
            # Create semi-transparent yellow surface
            highlight_surface = pygame.Surface((tile_rect.width, tile_rect.height))
            highlight_surface.set_alpha(100)  # Lower opacity (0-255, 100 = ~40% opacity)
            highlight_surface.fill(self.app.YELLOW)
            surface.blit(highlight_surface, tile_rect)
        
        # Highlight valid moves/builds for tutorial mode with semi-transparent green
        if self.app.is_tutorial_mode():
            highlighted_tiles = game.get_highlighted_tiles()
            current_tile = game.board.get_tile(Position(x, y))
            if current_tile in highlighted_tiles:
                # Create semi-transparent green surface
                highlight_surface = pygame.Surface((tile_rect.width, tile_rect.height))
                highlight_surface.set_alpha(120)  # Slightly more visible for tutorial
                highlight_surface.fill(self.app.GREEN)
                surface.blit(highlight_surface, tile_rect)
    
    def _render_game_info(self, surface: pygame.Surface) -> None:
        """Render game information like current phase."""
        game = self.app.get_game()
        if not game:
            return
        
        current_phase = game.turn_manager.get_phase()
        phase_text = f"Phase: {current_phase}"
        
        phase_surface = self.app.medium_font.render(phase_text, True, self.app.BLACK)
        surface.blit(phase_surface, (50, 150))
    
    def _render_god_cards(self, surface: pygame.Surface) -> None:
        """Render current player's god card large on the right side of the screen."""
        game = self.app.get_game()
        if not game or self.app.is_tutorial_mode():
            return
        
        current_player = game.turn_manager.current_player
        
        if current_player.god_card:
            god_name = current_player.god_card.name.lower()
            
            # Large god card position on the right side
            start_x = self.app.WINDOW_WIDTH - 530  
            start_y = 280 
            
            # God card background panel
            card_rect = pygame.Rect(start_x, start_y, 400, 450)
            panel_surface = pygame.Surface((card_rect.width, card_rect.height))
            panel_surface.set_alpha(200)
            panel_surface.fill((255, 255, 255))
            surface.blit(panel_surface, card_rect)
            pygame.draw.rect(surface, self.app.BLACK, card_rect, 3)
            
            # Player name at top
            name_text = self.app.medium_font.render(f"{current_player.player_name}'s God", True, self.app.BLACK)
            name_rect = name_text.get_rect(center=(card_rect.centerx, card_rect.y + 25))
            surface.blit(name_text, name_rect)
            
            # God card image 
            if god_name in self.god_card_images:
                god_image = self.god_card_images[god_name]
                image_rect = god_image.get_rect(center=(card_rect.centerx, card_rect.y + 240))
                surface.blit(god_image, image_rect)
            else:
                god_text = self.app.large_font.render(current_player.god_card.name, True, self.app.BLACK)
                god_rect = god_text.get_rect(center=(card_rect.centerx, card_rect.y + 200))
                surface.blit(god_text, god_rect)
    
    def _render_tutorial_elements(self, surface: pygame.Surface) -> None:
        """Render tutorial-specific UI elements."""
        # Tutorial instructions in a frame on the right side
        instructions = self.app.get_tutorial_instructions()
        if instructions:
            self._render_tutorial_instructions_frame(surface, instructions)
    
    def _render_tutorial_instructions_frame(self, surface: pygame.Surface, instructions: str) -> None:
        """Render tutorial instruction text in a large frame on the right side of the board."""

        board_offset_x = int(0.3 * self.app.WINDOW_WIDTH - (self.app.BOARD_W * self.app.TILE_SIZE) // 2)
        board_width = self.app.BOARD_W * self.app.TILE_SIZE
        board_right_edge = board_offset_x + board_width
        
        # Large instructions panel positioned to the right of the board with margin
        panel_x = board_right_edge + 150  
        panel_y = 315
        panel_width = 420
        panel_height = 400
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        # Semi-transparent white background panel
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(200)
        panel_surface.fill(self.app.WHITE)
        surface.blit(panel_surface, panel_rect)
        
        # Panel border with rounded corners
        pygame.draw.rect(surface, self.app.BLACK, panel_rect, 3)
        
        # Title
        title_text = self.app.large_font.render("Tutorial Instructions", True, self.app.BLACK)
        title_rect = title_text.get_rect(center=(panel_rect.centerx, panel_rect.y + 30))
        surface.blit(title_text, title_rect)
        
        # Instructions text with better formatting
        lines = instructions.split('\n')
        y_offset = panel_rect.y + 70
        line_height = 24
        
        for line in lines:
            if line.strip():  
                # Use different font size for headers vs content
                if line.startswith("Step") or line.startswith("Welcome"):
                    text = self.app.medium_font.render(line.strip(), True, self.app.BLACK)
                    # Center align step headers
                    text_rect = text.get_rect(center=(panel_rect.centerx, y_offset))
                    surface.blit(text, text_rect)
                else:
                    text = self.app.small_font.render(line.strip(), True, self.app.BLACK)
                    # Left align content with proper padding
                    surface.blit(text, (panel_rect.x + 15, y_offset))
                
                y_offset += line_height
                
                # Prevent text from going outside panel
                if y_offset > panel_rect.bottom - 30:
                    break
    
    def _render_standard_game_elements(self, surface: pygame.Surface) -> None:
        """Render standard game mode specific elements."""
        self._render_player_timers(surface)
    
    def _render_player_timers(self, surface: pygame.Surface) -> None:
        """Render player timers for standard games."""
        game = self.app.get_game()
        if not game or len(game.players) < 2:
            return
        
        # Get timer info 
        timer_info = game.get_all_players_timer_info()
        current_player = game.turn_manager.current_player
        
        # Player 1 timer (left side)
        player1 = game.players[0]
        if player1.player_name in timer_info and timer_info[player1.player_name]['remaining_time'] is not None:
            info1 = timer_info[player1.player_name]
            
            # Background color changes if it's the current player's turn
            bg_color = self.app.LIGHT_GREEN if player1 == current_player else self.app.LIGHT_GRAY
            
            # Warning color if time is low
            if info1['remaining_time'] and info1['remaining_time'] < 30:
                bg_color = self.app.LIGHT_RED
            
            # Timer box
            timer_rect1 = pygame.Rect(50, 30, 200, 60)
            pygame.draw.rect(surface, bg_color, timer_rect1)
            pygame.draw.rect(surface, self.app.BLACK, timer_rect1, 2)
            
            # Player name
            name_text1 = self.app.medium_font.render(player1.player_name, True, self.app.BLACK)
            name_rect1 = name_text1.get_rect(center=(timer_rect1.centerx, timer_rect1.y + 15))
            surface.blit(name_text1, name_rect1)
            
            # Timer display
            timer_text1 = self.app.large_font.render(info1['formatted_time'], True, self.app.BLACK)
            timer_text_rect1 = timer_text1.get_rect(center=(timer_rect1.centerx, timer_rect1.y + 40))
            surface.blit(timer_text1, timer_text_rect1)
        
        # Player 2 timer (right side)
        if len(game.players) >= 2:
            player2 = game.players[1]
            if player2.player_name in timer_info and timer_info[player2.player_name]['remaining_time'] is not None:
                info2 = timer_info[player2.player_name]
                
                # Background color changes if it's the current player's turn
                bg_color = self.app.LIGHT_GREEN if player2 == current_player else self.app.LIGHT_GRAY
                
                # Warning color if time is low
                if info2['remaining_time'] and info2['remaining_time'] < 30:
                    bg_color = self.app.LIGHT_RED
                
                # Timer box
                timer_rect2 = pygame.Rect(self.app.WINDOW_WIDTH - 250, 30, 200, 60)
                pygame.draw.rect(surface, bg_color, timer_rect2)
                pygame.draw.rect(surface, self.app.BLACK, timer_rect2, 2)
                
                # Player name
                name_text2 = self.app.medium_font.render(player2.player_name, True, self.app.BLACK)
                name_rect2 = name_text2.get_rect(center=(timer_rect2.centerx, timer_rect2.y + 15))
                surface.blit(name_text2, name_rect2)
                
                # Timer display
                timer_text2 = self.app.large_font.render(info2['formatted_time'], True, self.app.BLACK)
                timer_text_rect2 = timer_text2.get_rect(center=(timer_rect2.centerx, timer_rect2.y + 40))
                surface.blit(timer_text2, timer_text_rect2) 