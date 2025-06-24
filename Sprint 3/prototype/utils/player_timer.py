import time
from typing import Optional


class PlayerTimer:
    """Manages timer functionality for a player."""
    
    def __init__(self, time_limit_seconds: Optional[float]) -> None:
        """Initialize timer with a time limit."""
        self._time_limit = time_limit_seconds
        self._remaining_time = time_limit_seconds
        self._start_time: Optional[float] = None
        self._is_active = False
        self._is_expired = False
        self._has_timer = time_limit_seconds is not None
    
    @property
    def time_limit(self) -> Optional[float]:
        """Get the total time limit in seconds."""
        return self._time_limit
    
    @property
    def remaining_time(self) -> Optional[float]:
        """Get the remaining time in seconds."""
        if not self._has_timer:
            return None
            
        if self._is_active and self._start_time is not None:
            # Update remaining time based on elapsed time
            elapsed = time.time() - self._start_time
            self._remaining_time = max(0, self._remaining_time - elapsed)
            self._start_time = time.time()
            
            # Check if timer expired
            if self._remaining_time <= 0:
                self._is_expired = True
                self._is_active = False

        return self._remaining_time
    
    @property
    def is_active(self) -> bool:
        """Check if the timer is currently running."""
        return self._is_active and self._has_timer
    
    @property
    def is_expired(self) -> bool:
        """Check if the timer has expired."""
        return self._is_expired and self._has_timer
    
    def start(self) -> None:
        """Start the timer for the current turn."""
        if self._has_timer and not self._is_expired and self._remaining_time and self._remaining_time > 0:
            self._is_active = True
            self._start_time = time.time()
    
    def pause(self) -> None:
        """Pause the timer (called when turn ends)."""
        if self._has_timer and self._is_active:
            # Update remaining time before pausing
            _ = self.remaining_time 
            self._is_active = False
            self._start_time = None
    
    def reset(self) -> None:
        """Reset the timer to its initial state."""
        if self._has_timer:
            self._remaining_time = self._time_limit
            self._start_time = None
            self._is_active = False
            self._is_expired = False

    def get_formatted_time(self) -> str:
        """Get remaining time formatted as MM:SS."""
        if not self._has_timer:
            return ""  
            
        remaining = self.remaining_time
        if remaining is None:
            return ""
            
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        return f"{minutes:02d}:{seconds:02d}" 