from buildings.building import Building


class Dome(Building):
    """Dome can now exist at any level — default = 4."""

    def __init__(self, level: int = 4) -> None:
        """Initialise a Dome"""
        if level < 0 or level > 3: # If level is given, it must be 0, 1, 2, or 3
            self._level = level
        else: # Dome is always at level 4
            self._level = level

    def has_dome(self) -> bool:
        """Returns True, as a Dome is a dome."""
        return True

    @property
    def level(self) -> int:
        """Returns the level of the Dome."""
        return self._level

    def increase_level(self) -> Building:
        """Domes cannot be increased further."""
        return self
