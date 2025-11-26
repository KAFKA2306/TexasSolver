"""Data types for poker observations and actions.

This module defines the core data structures used throughout the poker GTO system,
following pamiq-core conventions.
"""

from dataclasses import dataclass
from enum import Enum


class GamePhase(Enum):
    """Poker game phases."""

    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"


@dataclass
class PokerObservation:
    """Poker observation data (pamiq-core compliant).

    Attributes:
        game_phase: Current phase of the game
        pot_size: Current pot size in chips
        effective_stack: Effective stack size for both players
        hole_cards: Player's hole cards (None during preflop)
        board_cards: Community cards on the board
        position: Player position ("IP" or "OOP")
        action_history: List of actions taken in current hand
        timestamp: Unix timestamp of observation
    """

    game_phase: GamePhase
    pot_size: float
    effective_stack: float
    hole_cards: tuple[str, str] | None
    board_cards: list[str]
    position: str
    action_history: list[str]
    timestamp: float
