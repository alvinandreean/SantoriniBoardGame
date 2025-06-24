from typing import List, Optional, TYPE_CHECKING

from tutorial.tutorial_step import TutorialStep
from tutorial.steps.introduction_step import IntroductionStep
from tutorial.steps.select_worker_step import SelectWorkerStep
from tutorial.steps.move_worker_step import MoveWorkerStep
from tutorial.steps.build_step import BuildStep
from tutorial.steps.move_to_level3_step import MoveToLevel3Step
from tutorial.steps.move_to_trap_step import MoveToTrapStep
from tutorial.steps.completion_step import CompletionStep
from tutorial.tutorial_observer import TutorialObserver

if TYPE_CHECKING:
    from core.player import Player
    from core.board import Board
    from core.worker import Worker
    from core.tile import Tile



class TutorialManager:
    """Manages tutorial progression and notifies observers."""
    
    def __init__(self, tutorial_type: str = "basic") -> None:
        """Initialize tutorial manager with steps based on tutorial type."""
        self._tutorial_type = tutorial_type
        self._current_step_index = 0
        self._observers: List[TutorialObserver] = []
        self._is_tutorial_complete = False
        self._introduction_clicked = False
        
        # Create step sequence based on tutorial type
        if tutorial_type == "basic":
            self._steps = [
                IntroductionStep(tutorial_type),
                SelectWorkerStep(),
                MoveWorkerStep(),
                BuildStep(),
                CompletionStep(tutorial_type)
            ]
            # Auto-advance past introduction for basic tutorial to show workers immediately
            self._current_step_index = 1  # Start at SelectWorkerStep
            self._introduction_clicked = True
            
        elif tutorial_type == "win":
            self._steps = [
                IntroductionStep(tutorial_type),
                MoveToLevel3Step(),
                CompletionStep(tutorial_type)
            ]
            # Auto-advance past introduction for win tutorial
            self._current_step_index = 1  # Start at MoveToLevel3Step
            self._introduction_clicked = True
            
        elif tutorial_type == "lose":
            self._steps = [
                IntroductionStep(tutorial_type),
                MoveToTrapStep(),
                CompletionStep(tutorial_type)
            ]
            # Auto-advance past introduction for lose tutorial
            self._current_step_index = 1  # Start at MoveToTrapStep
            self._introduction_clicked = True
        else:
            # Default to basic tutorial
            self._steps = [
                IntroductionStep("basic"),
                SelectWorkerStep(),
                MoveWorkerStep(),
                BuildStep(),
                CompletionStep("basic")
            ]
            # Auto-advance past introduction for default case too
            self._current_step_index = 1
            self._introduction_clicked = True
    
    def add_observer(self, observer: TutorialObserver) -> None:
        """Add an observer to be notified of tutorial events."""
        self._observers.append(observer)
    
    def remove_observer(self, observer: TutorialObserver) -> None:
        """Remove an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def get_current_step(self) -> Optional[TutorialStep]:
        """Get the current tutorial step."""
        if self._current_step_index < len(self._steps):
            return self._steps[self._current_step_index]
        return None
    
    def get_current_instructions(self) -> str:
        """Get instructions for the current step."""
        current_step = self.get_current_step()
        return current_step.get_instructions() if current_step else ""
    
    def is_valid_tile_click(self, tile: 'Tile', current_player: 'Player', current_worker: Optional['Worker'], phase: str) -> bool:
        """Check if a tile click is valid for the current tutorial step."""
        current_step = self.get_current_step()
        if not current_step:
            return True
        
        return current_step.is_valid_tile_click(tile, current_player, current_worker, phase)
    
    def get_highlighted_tiles(self, current_player: 'Player',current_worker: Optional['Worker'], phase: str, board: 'Board') -> List['Tile']:
        """Get tiles to highlight for the current step."""
        current_step = self.get_current_step()
        if not current_step:
            return []
        
        return current_step.get_highlighted_tiles(current_player, current_worker, phase, board)
    
    def handle_tile_click(self, current_player: 'Player', current_worker: Optional['Worker'], phase: str, board: 'Board') -> None:
        """Handle a tile click and advance tutorial if needed."""
        current_step = self.get_current_step()
        if not current_step:
            return
        
        if current_step.handles_click_progression() and not self._introduction_clicked:
            self._introduction_clicked = True
            self._advance_step()
            return
        
        # Check if current step is complete and should auto-advance
        if current_step.is_step_complete(current_player, current_worker, phase, board):
            if current_step.should_auto_advance():
                self._advance_step()
    
    def handle_step_tile_click(self, tile: 'Tile', current_player: 'Player', current_worker: Optional['Worker'], phase: str, board: 'Board') -> None:
        """Handle a specific tile click for custom step logic."""
        current_step = self.get_current_step()
        if current_step:
            # Call the step's custom tile click handler
            current_step.handle_tile_click(tile, current_player, current_worker, phase)
            
            # Check if step is now complete after the custom handling
            if current_step.is_step_complete(current_player, current_worker, phase, board):
                if current_step.should_auto_advance():
                    self._advance_step()
    
    def force_step_check(self, current_player: 'Player', current_worker: Optional['Worker'], phase: str, board: 'Board') -> None:
        """Force check if current step should advance - useful for tutorial progression."""
        current_step = self.get_current_step()
        if current_step and current_step.is_step_complete(current_player, current_worker, phase, board):
            if current_step.should_auto_advance():
                self._advance_step()
    
    def _advance_step(self) -> None:
        """Advance to the next tutorial step."""
        self._current_step_index += 1
        
        if self._current_step_index >= len(self._steps):
            # Tutorial completed
            self._is_tutorial_complete = True
            self._notify_tutorial_completed()
        else:
            # Notify observers of step change
            current_step = self.get_current_step()
            if current_step:
                self._notify_step_changed(current_step)
    
    def is_tutorial_complete(self) -> bool:
        """Check if the tutorial is complete."""
        return self._is_tutorial_complete
    
    def complete_tutorial(self) -> None:
        """Manually complete the tutorial."""
        self._is_tutorial_complete = True
        self._notify_tutorial_completed()
    
    def _notify_step_changed(self, step: TutorialStep) -> None:
        """Notify all observers that the tutorial step changed."""
        for observer in self._observers:
            observer.on_tutorial_step_changed(step)
    
    def _notify_tutorial_completed(self) -> None:
        """Notify all observers that the tutorial is completed."""
        for observer in self._observers:
            observer.on_tutorial_completed() 