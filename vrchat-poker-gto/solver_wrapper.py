#!/usr/bin/env python3
"""TexasSolver Simple Wrapper - MVP

The simplest possible wrapper to run TexasSolver from Python.
"""

import json
import subprocess
from pathlib import Path


def solve_poker_situation(
    hand: str,
    board: str,
    pot: float,
    stack: float,
    solver_path: str = "./TexasSolver",
    iterations: int = 20,
) -> dict:
    """Run TexasSolver and return strategy.

    Args:
        hand: Player's hole cards (e.g., "AsKh")
        board: Community cards (e.g., "Qs Jh 2h")
        pot: Pot size in chips
        stack: Effective stack size
        solver_path: Path to TexasSolver executable
        iterations: Number of CFR iterations (lower = faster, less accurate)

    Returns:
        Strategy dictionary with recommended actions and frequencies
    """
    # Generate config file
    config_content = f"""set_pot {pot}
set_effective_stack {stack}
set_board {board.replace(" ", ",")}
set_range_ip AA,KK,QQ,JJ,TT,99,88,77,AK,AQ,AJ
set_range_oop AA,KK,QQ,JJ,TT,99,88,77,AK,AQ,AJ
set_bet_sizes oop,flop,bet,50
set_bet_sizes ip,flop,bet,50
set_allin_threshold 0.67
build_tree
set_thread_num 4
set_accuracy 0.5
set_max_iteration {iterations}
start_solve
dump_result output_result.json
"""

    # Write temporary config
    config_path = Path("temp_solver_config.txt")
    config_path.write_text(config_content)

    try:
        # Run TexasSolver
        print(f"Running TexasSolver with {iterations} iterations...")
        result = subprocess.run(
            [solver_path, "--config", str(config_path)],
            capture_output=True,
            timeout=10,
            text=True,
        )

        # Check output
        output_path = Path("output_result.json")
        if output_path.exists():
            with open(output_path) as f:
                strategy = json.load(f)
            return strategy
        else:
            # Fallback: return raw output
            return {"error": "No output file", "raw_output": result.stdout[:500]}

    except subprocess.TimeoutExpired:
        return {"error": "Solver timeout"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Cleanup
        config_path.unlink(missing_ok=True)


def format_strategy(strategy: dict) -> str:
    """Format strategy for display."""
    if "error" in strategy:
        return f"Error: {strategy['error']}"

    lines = ["=== GTO RECOMMENDATION ==="]

    # 戦略抽出 (実際のJSON構造に応じて調整が必要)
    if "strategy" in strategy:
        for action, freq in strategy["strategy"].items():
            lines.append(f"{action.upper()}: {freq * 100:.1f}%")
    else:
        lines.append("Strategy data not found in output")
        lines.append(f"Keys available: {list(strategy.keys())}")

    lines.append("=" * 25)
    return "\n".join(lines)


def main():
    """Example usage."""
    print("TexasSolver Simple Wrapper - MVP\n")

    # Example situation
    result = solve_poker_situation(hand="AsKh", board="Qs Jh 2h", pot=50, stack=200, iterations=20)

    print(format_strategy(result))

    # Also save raw JSON
    with open("last_result.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\nFull result saved to: last_result.json")


if __name__ == "__main__":
    main()
