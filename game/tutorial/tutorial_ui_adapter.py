from tutorial.tutorial_observer import TutorialObserver
from tutorial.tutorial_step import TutorialStep


class TutorialUIAdapter(TutorialObserver):
    """Adapter to bridge tutorial events to main app UI updates."""
    
    def __init__(self, app):
        self._app = app
    
    def on_tutorial_step_changed(self, step: TutorialStep) -> None:
        """Called when tutorial step changes."""
        self._app.update_tutorial_ui()
    
    def on_tutorial_completed(self) -> None:
        """Called when tutorial is completed."""
        self._app.show_message("Tutorial completed! Well done!")
