from typing import List, Optional

from game_modes.game_mode import GameMode
from core.player import Player
from core.board import Board
from core.tile import Tile
from core.worker import Worker
from core.position import Position
from tutorial.tutorial_manager import TutorialManager
from buildings.block import Block

class TutorialGameMode(GameMode):
    """
    Tutorial game mode implementation.
    Uses predefined board setup and tutorial manager for guided gameplay.
    """
    
    def __init__(self, tutorial_type: str = "basic") -> None:
        """Initialize tutorial mode with tutorial manager."""
        self._tutorial_manager = TutorialManager(tutorial_type)
        self._tutorial_type = tutorial_type
    
    @property
    def tutorial_manager(self) -> TutorialManager:
        """Get the tutorial manager."""
        return self._tutorial_manager
    
    def initialize_game(self, players: List[Player], board: Board) -> None:
        """Initialize tutorial with predefined setup."""
        if len(players) < 1:
            raise ValueError("Tutorial mode requires at least one player")
        
        # Use only the first player for tutorial
        tutorial_player = players[0]
        
        # Set up predefined board layout for tutorial
        self._setup_tutorial_board(tutorial_player, board)
    
    def is_valid_tile_click(self, tile: Tile, current_player: Player, current_worker: Optional[Worker], phase: str) -> bool:
        """Check if tile click is valid according to tutorial step."""
        # Block ALL actions if tutorial is complete
        if self._tutorial_manager.is_tutorial_complete():
            return False
        
        # Restrict worker selection in ALL tutorial types during "Select Worker" phase
        if phase == "Select Worker":
            return self._tutorial_manager.is_valid_tile_click(tile, current_player, current_worker, phase)
        
        # For other phases, let tutorial manager decide
        return self._tutorial_manager.is_valid_tile_click(tile, current_player, current_worker, phase)
    
    def get_guidance_message(self, current_player: Player, current_worker: Optional[Worker], phase: str) -> Optional[str]:
        """Get guidance message from current tutorial step."""
        return self._tutorial_manager.get_current_instructions()
    
    def get_highlighted_tiles(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> List[Tile]:
        """Get highlighted tiles from current tutorial step."""
        return self._tutorial_manager.get_highlighted_tiles(current_player, current_worker, phase, board)
    
    def should_end_game(self) -> bool:
        """Tutorial ends when tutorial manager indicates completion."""
        # End immediately when tutorial step is complete - no more phases
        return self._tutorial_manager.is_tutorial_complete()
    
    def get_mode_name(self) -> str:
        """Get the mode name."""
        return "Tutorial"
    
    def handle_post_action_update(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> None:
        """Handle post-action updates for tutorial progression."""
        # Do normal tutorial progression first
        self._tutorial_manager.handle_tile_click(current_player, current_worker, phase, board)
        self._tutorial_manager.force_step_check(current_player, current_worker, phase, board)
        
        # Only check for tutorial completion if we're at the final step and it's complete
        current_step = self._tutorial_manager.get_current_step()
        if (current_step and 
            current_step.get_step_name() == "Tutorial Complete" and 
            current_step.is_step_complete(current_player, current_worker, phase, board)):
            # Force tutorial completion to end game only for completion step
            self._tutorial_manager.complete_tutorial()
    
    def handle_tile_click(self, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> None:
        """Handle tile click for tutorial progression."""
        # This handles the standard tutorial progression
        self._tutorial_manager.handle_tile_click(current_player, current_worker, phase, board)
    
    def handle_tile_click_with_tile(self, tile: Tile, current_player: Player, current_worker: Optional[Worker], phase: str, board: Board) -> None:
        """Handle tile click with specific tile for custom tutorial logic."""
        # Call both the standard progression and the custom tile click handler
        self._tutorial_manager.handle_tile_click(current_player, current_worker, phase, board)
        self._tutorial_manager.handle_step_tile_click(tile, current_player, current_worker, phase, board)
    
    def _setup_tutorial_board(self, player: Player, board: Board) -> None:
        """Set up predefined board layout for tutorial."""
        # Clear the board first
        self._clear_board(board)
        
        if self._tutorial_type == "basic":
            # Basic tutorial setup - original layout
            # Place tutorial player's workers at strategic positions
            worker_positions = [Position(1, 1), Position(1, 3)]
            
            for i, pos in enumerate(worker_positions):
                tile = board.get_tile(pos)
                worker = Worker(pos, player.player_color)
                player.add_worker(worker)
                tile.worker = worker
            
            # Set up structures for progressive learning
            # Basic level 1 building at (2,2) for initial building practice
            level1_tile = board.get_tile(Position(2, 2))
            level1_tile.building = Block(1)
            
            # Level 2 building at (3,1) - for building practice
            level2_tile = board.get_tile(Position(3, 1))
            level2_tile.building = Block(2)
            
            # Pre-existing level 3 building at (4,4) to show final goal
            level3_tile = board.get_tile(Position(4, 4))
            level3_tile.building = Block(3)
            
            # Add some variety with additional structures
            extra_level1 = board.get_tile(Position(0, 2))
            extra_level1.building = Block(1)
            
            extra_level2 = board.get_tile(Position(2, 4))
            extra_level2.building = Block(2)
            
        elif self._tutorial_type == "win":
            # Win tutorial setup - focus on positioning for victory
            # Place workers strategically for winning scenario
            # Worker 1 at (2,2) - on a level 2 building (ready to climb to level 3)
            # Worker 2 at (1,1) - ground level
            worker1_pos = Position(2, 2)
            worker2_pos = Position(1, 1)
            
            # Place worker 1 on level 2 building
            level2_tile = board.get_tile(worker1_pos)
            level2_tile.building = Block(2)
            worker1 = Worker(worker1_pos, player.player_color)
            player.add_worker(worker1)
            level2_tile.worker = worker1
            
            # Place worker 2 on ground
            worker2_tile = board.get_tile(worker2_pos)
            worker2 = Worker(worker2_pos, player.player_color)
            player.add_worker(worker2)
            worker2_tile.worker = worker2
            
            # Set up the winning target - level 3 building at (3,3) adjacent to worker 1
            target_tile = board.get_tile(Position(3, 3))
            target_tile.building = Block(3)
            
            # Add some other buildings for context
            # Level 1 buildings
            board.get_tile(Position(0, 0)).building = Block(1)
            board.get_tile(Position(4, 4)).building = Block(1)
            
            # Another level 2 building
            board.get_tile(Position(1, 4)).building = Block(2)
            
        elif self._tutorial_type == "lose":
            # Lose tutorial setup - height-based trap scenario
            # Worker 1: bottom right, surrounded by opponents and dome (already trapped)
            # Worker 2: on level 2 building at (1,1), will be forced to move to (0,0) and get trapped by height
            
            # Place player worker 1 at bottom right (4,4) - already trapped
            worker1_pos = Position(4, 4)
            worker1_tile = board.get_tile(worker1_pos)
            worker1 = Worker(worker1_pos, player.player_color)
            player.add_worker(worker1)
            worker1_tile.worker = worker1
            
            # Place player worker 2 at (1,1) on level 2 building
            worker2_pos = Position(1, 1)
            worker2_tile = board.get_tile(worker2_pos)
            worker2_tile.building = Block(2)  # Level 2 building
            worker2 = Worker(worker2_pos, player.player_color)
            player.add_worker(worker2)
            worker2_tile.worker = worker2
            
            # Create the height trap around (1,1)
            # Domes at (1,0) and (0,1) - can't move to these
            from buildings.dome import Dome
            
            dome_tile_1 = board.get_tile(Position(1, 0))
            dome_tile_1.building = Dome()  # Dome at level 4
            
            dome_tile_2 = board.get_tile(Position(0, 1))
            dome_tile_2.building = Dome()  # Dome at level 4
            
            # Position (0,0) stays empty - this is the trap destination
            # When worker moves from level 2 to level 0, can't climb back up!
            
            # Surround worker 1 at (4,4) to make it completely blocked
            from colors.color import Color
            
            # Opponent workers around (4,4) - only 2 workers now
            opponent_positions = [
                Position(3, 3), Position(3, 4)
            ]
            
            for pos in opponent_positions:
                if pos.x < board.width and pos.y < board.height:
                    tile = board.get_tile(pos)
                    opponent_worker = Worker(pos, Color.RED)
                    tile.worker = opponent_worker
            
            # Add a dome at (4,3) to complete the trap around worker 1
            dome_blocking_worker1 = board.get_tile(Position(4, 3))
            dome_blocking_worker1.building = Dome()  # Dome to block worker 1
            
        else:
            # Default to basic setup for any other tutorial type
            worker_positions = [Position(1, 1), Position(1, 3)]
            
            for i, pos in enumerate(worker_positions):
                tile = board.get_tile(pos)
                worker = Worker(pos, player.player_color)
                player.add_worker(worker)
                tile.worker = worker
    
    def _clear_board(self, board: Board) -> None:
        """Clear all workers and buildings from the board."""
        for x in range(board.width):
            for y in range(board.height):
                tile = board.get_tile(Position(x, y))
                tile.worker = None
                tile.building = None 