from typing import List, Optional
import random

from game_modes.game_mode import GameMode
from core.player import Player
from core.board import Board
from core.tile import Tile
from core.worker import Worker


class StandardGameMode(GameMode):
    """
    Standard game mode implementation.
    Provides default behavior for normal Santorini gameplay.
    """
    
    def initialize_game(self, players: List[Player], board: Board) -> None:
        """Initialize standard game with random worker placement and god cards."""
        # Place workers randomly for each player
        for player in players:
            self._place_random_workers(player, board)
    
    def is_valid_tile_click(self, tile: Tile, current_player: Player, 
                           current_worker: Optional[Worker], phase: str) -> bool:
        """In standard mode, all valid moves are allowed."""
        return True  # Let the game's normal validation handle this
    
    def get_guidance_message(self, current_player: Player, 
                            current_worker: Optional[Worker], phase: str) -> Optional[str]:
        """Standard mode provides no guidance messages."""
        return None
    
    def get_highlighted_tiles(self, current_player: Player, 
                             current_worker: Optional[Worker], 
                             phase: str, board: Board) -> List[Tile]:
        """Standard mode highlights no tiles."""
        return []
    
    def should_end_game(self) -> bool:
        """Standard mode only ends on normal win conditions."""
        return False
    
    def get_mode_name(self) -> str:
        """Get the mode name."""
        return "Standard"
    
    def handle_post_action_update(self, current_player: Player, 
                                 current_worker: Optional[Worker], 
                                 phase: str, board: Board) -> None:
        """Standard mode doesn't need post-action updates."""
        pass  # No special handling needed for standard mode
    
    def _place_random_workers(self, player: Player, board: Board) -> None:
        """Places two workers randomly on the board for a player."""
        # Get all empty tiles on the board and shuffle them.
        tiles = board.get_all_empty_tiles()
        random.shuffle(tiles)
        
        # Place two workers on the first two shuffled tiles.
        for tile in tiles[:2]:
            worker = Worker(tile.position, player.player_color)
            # Assign the worker to the tile and add it to the player.
            player.add_worker(worker)
            tile.worker = worker 