from __future__ import annotations

from functools import total_ordering
from typing import Optional

from .charNormaliser import CharNormaliser


@total_ordering
class UnicodeBlock:
    def __init__(
        self,
        name: str,
        start: int,
        end: int,
        assigned_ranges: Optional[list[tuple[int, int]]] = None,
        aliases: Optional[list[str]] = None,
    ):
        self.name = name
        self.start = start
        self.end = end
        self.assigned_ranges = AssignedRanges(assigned_ranges) if assigned_ranges else []
        self.aliases = [self.normalise_name(a) for a in aliases] if aliases else []

    @property
    def normalised_name(self) -> str:
        """Return the normalised name of this Unicode block."""
        return self.normalise_name(self.name)

    @property
    def variable_name(self) -> str:
        """Return the variable name of this Unicode block."""
        return self.to_variable_name(self.name)

    def __contains__(self, char: str | int | bytes) -> bool:
        """Check if a character is in this Unicode block.
        May be a str, int, or bytes. Bytes are decoded to str using utf-8."""
        unidec = CharNormaliser.to_codepoint(char)
        return self.start <= unidec <= self.end

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UnicodeBlock):
            return NotImplemented
        return self.start == other.start

    def __lt__(self, other: object) -> bool:
        """Compare two UnicodeBlock objects based on their start values."""
        if not isinstance(other, UnicodeBlock):
            return NotImplemented
        return self.start < other.start

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __repr__(self) -> str:
        parts = [
            f"name={self.name!r}",
            f"start={self.start:#06x}",
            f"end={self.end:#06x}",
        ]

        if self.assigned_ranges:
            ranges_str = [f"({start:#06x}, {end:#06x})" for start, end in self.assigned_ranges]
            parts.append(f"assigned_ranges=[{', '.join(ranges_str)}]")

        if self.aliases:
            parts.append(f"aliases={self.aliases!r}")

        return f"{self.__class__.__name__}({', '.join(parts)})"

    def __len__(self) -> int:
        """Return the number of available code points in this block."""
        return self.end - self.start + 1

    @staticmethod
    def normalise_name(name: str) -> str:
        """Normalise the name of a Unicode block."""
        name = name.upper().replace(" ", "").replace("-", "").replace("_", "")
        if name.startswith("IS"):
            name = name[2:]
        return name

    @staticmethod
    def to_variable_name(name: str) -> str:
        """Normalise the variable name of a Unicode block."""
        return name.upper().replace(" ", "_").replace("-", "_")

class AssignedRanges:
    """A class to represent assigned ranges within a Unicode block."""
    
    def __init__(self, ranges: list[tuple[int, int]]):
        self.ranges = ranges

    def __iter__(self):
        return iter(self.ranges)

    def __repr__(self) -> str:
        return f"AssignedRanges({self.ranges})"
    
    def __len__(self) -> int:
        """Return the number of assigned ranges."""
        if self.ranges is None:
            return 0
        return sum(end - start + 1 for start, end in self.ranges)
    
    def __contains__(self, char: str | int | bytes) -> bool:
        """Check if a character is in any of the assigned ranges."""
        unidec = CharNormaliser.to_codepoint(char)
        for start, end in self.ranges:
            if start <= unidec <= end:
                return True
        return False