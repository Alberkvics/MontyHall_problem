"""
simulation.py - Simulation mode: runs N games automatically
"""

import random
from src.game import play_one_game
from src.display import C, show_simulation_results, show_separator

N_DOORS = 3


def run_simulation(n_games: int = 1000,
                   verbose: bool = False,
                   rng: random.Random = None):
    """
    Simulates n_games rounds, alternating between switching and staying
    Records empirical win rates for both strategies
    Also records the cumulative switch history for the convergence table
    """
    rng = rng or random.Random()

    wins_switch = 0
    wins_stay = 0
    losses_switch = 0
    losses_stay = 0

    ## TRACKS CUMULATIVE SWITCH AT EACH GAME INDEX - USED BY CONVERGENCE TABLE
    switch_wins_history = []

    print()
    show_separator("═")
    print(C.bold(C.cyan(f"  ⚙️  SIMULATING {n_games} GAMES...")))
    show_separator("═")

    ## VISUAL PROGRESS
    milestones = set()
    if n_games >= 10:
        step = max(n_games // 10, 1)
        milestones = set(range(step, n_games + 1, step))

    for i in range(1, n_games + 1):
        ## HALF THE GAMES WITH SWITCH = TRUES, HALF WITH SWITCH = FALSE
        switch = (i % 2 == 0)
        state = play_one_game(n_doors=N_DOORS, switch=switch, rng=rng)

        if switch:
            if state.won: wins_switch  += 1
            else:         losses_switch += 1
            ## RECORD CUMULATIVE SWITCH RESULT AFTER EACH SWITCH GAME
            switch_wins_history.append(wins_switch)
        else:
            if state.won: wins_stay  += 1
            else:         losses_stay += 1

        if verbose and i in milestones:
            done = i / n_games
            filled = round(done * 30)
            bar = f"{C.CYAN}{'█' * filled}{C.DIM}{'░' * (30 - filled)}{C.RESET}"
            gs  = wins_switch + losses_switch
            gst = wins_stay   + losses_stay
            rs  = wins_switch / gs  if gs  else 0
            rst = wins_stay  / gst  if gst else 0
            print(
                f"  {bar}  {i:>6}/{n_games}  "
                f"switch={C.green(f'{rs:.1%}')}  "
                f"stay={C.red(f'{rst:.1%}')}",
                end="\r"
            )

    if verbose:
        print()  # clear the \r line

    show_simulation_results(
        n_games, N_DOORS,
        wins_switch, wins_stay,
        losses_switch, losses_stay
    )

    _show_convergence_table(switch_wins_history, N_DOORS)


def _show_convergence_table(switch_wins_history: list[int], n_doors: int):
    """
    Shows how the empirical win rate converged toward (n - 1) / n during
    the actual simulation — using the real recorded history, not a replay
    """
    teoria_switch = 1 - (1 / n_doors)
    n_switch_games = len(switch_wins_history)

    checkpoints = [10, 50, 100, 500, 1000, 5000, 10000]
    checkpoints = [c for c in checkpoints if c <= n_switch_games]
    if not checkpoints:
        return

    print(C.bold("  CONVERGENCE — win rate when always switching:\n"))
    print(C.dim(f"  {'N games':>8}  {'Empirical rate':>14}  {'Error vs theory':>15}  {'Bar'}"))
    print(C.dim("  " + "─" * 58))

    for n in checkpoints:
        ## SWITCH_WINS_HISTORY[N - 1] = CUMULATIVE WINS AFTER N SWITCH GAMES
        wins  = switch_wins_history[n - 1]
        rate  = wins / n
        error = abs(rate - teoria_switch)
        filled = round(rate * 24)
        bar = f"{C.GREEN}{'█' * filled}{C.DIM}{'░' * (24 - filled)}{C.RESET}"
        marker = C.green(f" ✓ ~{teoria_switch:.2%}") if error < 0.01 else ""
        print(
            f"  {n:>8}  {rate:>13.4f}   {error:>14.4f}  {bar}{marker}"
        )

    print()
    print(C.dim(f"  Theoretical value: {teoria_switch} ≈ {teoria_switch:.4f}"))
    print()


def ask_simulation_params() -> tuple[int, bool]:
    """Asks the user how many games to simulate."""
    print()
    print(C.bold("  How many games to simulate?"))
    print(f"  {C.cyan('[1]')}   100 games  (fast)")
    print(f"  {C.cyan('[2]')} 1,000 games")
    print(f"  {C.cyan('[3]')} 10,000 games (more accurate)")
    print(f"  {C.cyan('[4]')} Enter manually")
    print()

    choices = {"1": 100, "2": 1000, "3": 10000}

    while True:
        ans = input("  Option: ").strip()
        if ans in choices:
            n = choices[ans]
            break
        if ans == "4":
            try:
                n = int(input("  Number of games: ").strip())
                if n > 0:
                    break
            except ValueError:
                pass
        print(C.red("  Invalid option."))

    verbose = n >= 500
    return n, verbose
