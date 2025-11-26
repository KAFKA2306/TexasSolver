"""Data types for poker actions.

This module defines action-related data structures for the poker GTO system,
following pamiq-core conventions.
"""

from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    """Poker action types."""

    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALLIN = "allin"


@dataclass
class PokerAction:
    """Poker action data (pamiq-core compliant).

    Attributes:
        type: Type of action to take
        amount: Bet/raise amount in chips (None for non-betting actions)
        frequency: GTO recommended frequency for this action (0.0-1.0)
    """

    type: ActionType
    amount: float | None = None
    frequency: float = 1.0

    def __post_init__(self):
        """Validate action data."""
        if self.frequency < 0.0 or self.frequency > 1.0:
            raise ValueError(f"Frequency must be between 0.0 and 1.0, got {self.frequency}")

        if self.type in (ActionType.BET, ActionType.RAISE, ActionType.ALLIN):
            if self.amount is None or self.amount <= 0:
                raise ValueError(f"{self.type.value} requires positive amount")
