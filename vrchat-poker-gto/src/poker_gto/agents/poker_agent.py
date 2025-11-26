"""Poker Agent implementation."""

import time
from typing import override

from pamiq_core import Agent

from ..data.actions import ActionType, PokerAction
from ..data.observations import GamePhase, PokerObservation


class PokerAgent(Agent[PokerObservation, PokerAction]):
    """Agent that plays poker using GTO strategies."""

    def __init__(self):
        super().__init__()
        # Models will be attached later by the launcher
        self.solver_model = None

    @override
    def on_inference_models_attached(self) -> None:
        """Retrieve attached models."""
        self.solver_model = self.get_inference_model("texassolver")

    @override
    def step(self, observation: PokerObservation) -> PokerAction:
        """Decide next action based on observation."""

        # Preflop logic (Placeholder for now)
        if observation.game_phase == GamePhase.PREFLOP:
            # Simple default for preflop
            return PokerAction(type=ActionType.FOLD, frequency=1.0)

        # Postflop logic using TexasSolver
        if self.solver_model:
            strategy = self.solver_model.infer(observation)

            # Select best action (highest frequency)
            best_action = max(strategy.items(), key=lambda x: x[1])
            action_name = best_action[0].lower()
            frequency = best_action[1]

            # Map string to ActionType
            action_type = ActionType.FOLD
            amount = None

            if "check" in action_name:
                action_type = ActionType.CHECK
            elif "call" in action_name:
                action_type = ActionType.CALL
            elif "bet" in action_name:
                action_type = ActionType.BET
                amount = 50.0  # Should parse amount from strategy key if available
            elif "raise" in action_name:
                action_type = ActionType.RAISE
                amount = 100.0  # Placeholder
            elif "all" in action_name:  # All-in
                action_type = ActionType.ALLIN

            return PokerAction(type=action_type, amount=amount, frequency=frequency)

        return PokerAction(type=ActionType.CHECK, frequency=1.0)
