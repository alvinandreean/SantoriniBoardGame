from typing import List, Optional, Dict, TypedDict
from core.player import Player



class TimerInfo(TypedDict):
    """Type definition for timer information dictionary."""
    player_name: str
    remaining_time: float
    formatted_time: str
    is_expired: bool


class PlayerTimerInfo(TypedDict):
    """Type definition for individual player timer information."""
    remaining_time: float
    formatted_time: str
    is_expired: bool
    is_active: bool


class TimerManager:
    """
    Manages timer coordination across multiple players.

    Coordinates timer start/pause between players during turn transitions.
    """
    
    def __init__(self, players: List[Player]) -> None:
        """Initialize timer manager with list of players."""
        self._players = players
        self._current_timer_player: Optional[Player] = None
    
    @property
    def current_timer_player(self) -> Optional[Player]:
        """Get the player whose timer is currently active."""
        return self._current_timer_player
    
    def start_player_timer(self, player: Player) -> None:
        """Start the specified player's timer. """
        # Pause current timer
        self._pause_current_timer()
        
        # Start new player's timer
        player.start_timer()
        self._current_timer_player = player
    
    def pause_current_timer(self) -> None:
        """Pause the currently active timer."""
        self._pause_current_timer()
    
    def _pause_current_timer(self) -> None:
        """Internal method to pause current timer."""
        if self._current_timer_player:
            self._current_timer_player.pause_timer()
    
    def switch_timer_to_player(self, player: Player) -> None:
        """
        Switch timer from current player to specified player.
        Pauses current timer and starts new player's timer.
        """
        self.start_player_timer(player)
    
    def get_current_player_timer_info(self) -> Optional[TimerInfo]:
        """Get timer information for the currently active player."""
        if not self._current_timer_player:
            return None
            
        remaining_time = self._current_timer_player.get_remaining_time()
        return {
            'player_name': self._current_timer_player.player_name,
            'remaining_time': remaining_time,
            'formatted_time': self._format_time(remaining_time),
            'is_expired': remaining_time is not None and remaining_time <= 0
        }
    
    def get_all_players_timer_info(self) -> Dict[str, PlayerTimerInfo]:
        """
        Get timer information for all players.
        
        Dictionary mapping player names to their timer info
        """
        timer_info = {}
        
        for player in self._players:
            remaining_time = player.get_remaining_time()
            timer_info[player.player_name] = {
                'remaining_time': remaining_time,
                'formatted_time': self._format_time(remaining_time),
                'is_expired': remaining_time is not None and remaining_time <= 0,
                'is_active': player == self._current_timer_player
            }
        
        return timer_info
    
    def check_for_timer_expiration(self) -> Optional[Player]:
        """Check if any player's timer has expired."""
        for player in self._players:
            remaining_time = player.get_remaining_time()
            if remaining_time is not None and remaining_time <= 0:
                return player
        return None
    
    def has_any_timer_expired(self) -> bool:
        """Check if any player's timer has expired."""
        return self.check_for_timer_expiration() is not None
    
    def get_expired_players(self) -> List[Player]:
        """Get list of all players whose timers have expired."""
        expired_players = []
        for player in self._players:
            remaining_time = player.get_remaining_time()
            if remaining_time is not None and remaining_time <= 0:
                expired_players.append(player)
        return expired_players
    
    def _format_time(self, seconds: Optional[float]) -> str:
        """Format time in seconds to MM:SS string format."""
        if seconds is None:
            return "∞"  
            
        if seconds <= 0:
            return "00:00"
        
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes:02d}:{remaining_seconds:02d}"
    
    def reset_all_timers(self) -> None:
        """Reset all player timers to their initial state."""
        self._pause_current_timer()
        self._current_timer_player = None
