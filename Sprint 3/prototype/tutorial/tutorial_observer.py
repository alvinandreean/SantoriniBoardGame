from abc import ABC, abstractmethod
from tutorial.tutorial_step import TutorialStep

class TutorialObserver(ABC):
    """Observer interface for tutorial events."""
    
    @abstractmethod
    def on_tutorial_step_changed(self, step: TutorialStep) -> None:
        """Called when tutorial step changes."""
        pass
    
    @abstractmethod
    def on_tutorial_completed(self) -> None:
        """Called when tutorial is completed."""
        pass
