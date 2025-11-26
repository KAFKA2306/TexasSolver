"""TexasSolver model implementation for pamiq-core.

This module wraps the TexasSolver CLI as a pamiq-core InferenceWrappedModel.
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, override

from pamiq_core import InferenceWrappedModel

from ..data.actions import PokerAction
from ..data.observations import PokerObservation


class TexasSolverModel(InferenceWrappedModel[PokerObservation, dict[str, float]]):
    """TexasSolver wrapper model.

    Takes a PokerObservation and returns a strategy dictionary (action -> frequency).
    """

    def __init__(
        self,
        solver_path: str = "./TexasSolver",
        iterations: int = 20,
        threads: int = 4,
    ):
        """Initialize the model.

        Args:
            solver_path: Path to TexasSolver executable
            iterations: Number of CFR iterations
            threads: Number of threads to use
        """
        super().__init__()
        self.solver_path = solver_path
        self.iterations = iterations
        self.threads = threads
        self._cache: dict[str, dict[str, float]] = {}

    def _generate_config(self, obs: PokerObservation, config_path: Path) -> None:
        """Generate TexasSolver configuration file."""
        # Note: This is a simplified config generation for MVP.
        # In a real scenario, we need to map ranges and board cards accurately.

        # Convert board cards list to string
        board_str = ",".join(obs.board_cards) if obs.board_cards else ""

        config_content = f"""set_pot {obs.pot_size}
set_effective_stack {obs.effective_stack}
set_board {board_str}
set_range_ip AA,KK,QQ,JJ,TT,99,88,77,AK,AQ,AJ
set_range_oop AA,KK,QQ,JJ,TT,99,88,77,AK,AQ,AJ
set_bet_sizes oop,flop,bet,50
set_bet_sizes ip,flop,bet,50
set_allin_threshold 0.67
build_tree
set_thread_num {self.threads}
set_accuracy 0.5
set_max_iteration {self.iterations}
start_solve
dump_result output_result.json
"""
        config_path.write_text(config_content)

    def _get_cache_key(self, obs: PokerObservation) -> str:
        """Generate a cache key from observation."""
        # Simple cache key based on critical game state
        board = ",".join(sorted(obs.board_cards)) if obs.board_cards else ""
        hole = ",".join(sorted(obs.hole_cards)) if obs.hole_cards else ""
        return f"{hole}|{board}|{obs.pot_size}|{obs.effective_stack}"

    @override
    def infer(self, input_data: PokerObservation) -> dict[str, float]:
        """Run TexasSolver and return strategy."""

        # Check cache
        cache_key = self._get_cache_key(input_data)
        if cache_key in self._cache:
            return self._cache[cache_key]

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config_path = tmp_path / "solver_config.txt"
            output_path = Path("output_result.json")  # TexasSolver dumps to CWD usually

            self._generate_config(input_data, config_path)

            try:
                subprocess.run(
                    [self.solver_path, "--config", str(config_path)],
                    capture_output=True,
                    timeout=5.0,  # Strict timeout for real-time
                    text=True,
                    cwd=tmp_path,  # Run in temp dir to avoid clutter
                )

                # Read result from the temp dir (since we changed CWD)
                result_file = tmp_path / "output_result.json"
                if result_file.exists():
                    with open(result_file) as f:
                        data = json.load(f)
                        strategy = data.get("strategy", {})
                        self._cache[cache_key] = strategy
                        return strategy

            except subprocess.TimeoutExpired:
                print("TexasSolver timed out")
            except Exception as e:
                print(f"TexasSolver error: {e}")

        # Fallback strategy (Check/Fold)
        return {"check": 1.0, "fold": 0.0}

    @override
    def get_state_dict(self) -> dict[str, Any]:
        return {
            "solver_path": self.solver_path,
            "iterations": self.iterations,
            "threads": self.threads,
        }

    @override
    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        self.solver_path = state_dict.get("solver_path", self.solver_path)
        self.iterations = state_dict.get("iterations", self.iterations)
        self.threads = state_dict.get("threads", self.threads)
