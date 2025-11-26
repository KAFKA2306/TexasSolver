"""VRChat Poker Environment."""

from typing import override

from pamiq_core import Environment

from ..data.actions import PokerAction
from ..data.observations import PokerObservation
from .actuators import OSCActuator
from .sensors import PokerStateSensor, ScreenCaptureSensor


class VRChatPokerEnvironment(Environment[PokerObservation, PokerAction]):
    """Environment representing the VRChat Poker world."""

    def __init__(self):
        super().__init__()
        self.screen_sensor = ScreenCaptureSensor()
        self.state_sensor = PokerStateSensor(self.screen_sensor)
        self.osc_actuator = OSCActuator()

    @override
    def observe(self) -> PokerObservation:
        """Get current state from VRChat."""
        return self.state_sensor.read()

    @override
    def affect(self, action: PokerAction) -> None:
        """Execute action in VRChat."""
        self.osc_actuator.operate(action)
