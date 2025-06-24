from typing import List

from colors.color import Color
from core.worker import Worker
from utils.player_timer import PlayerTimer



class Player:
    """Represents a player in the Santorini game."""
    
    def __init__(self, name: str, age: int, color: Color, workers: List[Worker] | None = None, god_card = None, timer_seconds: float = 300) -> None:
        """Initializes a player with a name, age, color, workers and it's god card."""
        self._player_name = name
        self._player_age = age
        self._player_god = god_card
        self._player_color = color
        self._timer = PlayerTimer(timer_seconds)
        
        # If the workers passed are, create an empty list to hold the workers.
        if workers is None:
            self.workers= []
        
        # If the workers passed are not empty, check if they are valid (maximum 2 workers).
        elif len(workers) != 2: 
            raise ValueError("A player must have exactly two workers.")
        
        # If the workers passed are valid, assign them to the player.
        else:
            self.workers = workers

    @property
    def player_name(self) -> str:
        """Returns the name of the player."""
        return self._player_name
    
    @property
    def player_color(self) -> Color:
        """Returns the color of the player."""
        return self._player_color
    
    @property
    def god_card(self):
        return self._player_god
    
    def add_worker(self, worker: Worker) -> None:
        """Adds a worker to the player."""
        if len(self.workers) >= 2: # Check if the player already has two workers.
            raise ValueError("Cannot add more than two workers to a player.")
        self.workers.append(worker)

    @property
    def all_workers(self) -> List[Worker]:
        """Returns all workers that are assigned to the player."""
        return self.workers

    @property
    def timer(self) -> PlayerTimer:
        """Returns the player's timer."""
        return self._timer
    
    def set_timer(self, timer_seconds: float) -> None:
        """Set or update the player's timer."""
        self._timer = PlayerTimer(timer_seconds)
    
    def start_timer(self) -> None:
        """Start the player's timer for their turn."""
        self._timer.start()
    
    def pause_timer(self) -> None:
        """Pause the player's timer when their turn ends."""
        self._timer.pause()
    
    def get_remaining_time(self) -> float:
        """Get the player's remaining time in seconds."""
        return self._timer.remaining_time
    
    def get_formatted_time(self) -> str:
        """Get the player's remaining time formatted as MM:SS."""
        return self._timer.get_formatted_time()
    
    def is_timer_expired(self) -> bool:
        """Check if the player's timer has expired."""
        return self._timer.is_expired