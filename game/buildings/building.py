from abc import ABC, abstractmethod



class Building(ABC):
    """Abstract base for any kind of building that sits on a Tile."""

    @abstractmethod
    def has_dome(self) -> bool:
        """Returns True if the building is a Dome."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def level(self) -> int:
        """Returns the level of the building."""
        raise NotImplementedError()

    @abstractmethod
    def increase_level(self):
        """ 
        Attempt to raise the building by one level.
        
        Returns a new Building (self or Dome) to replace the old one.
        """
        raise NotImplementedError()