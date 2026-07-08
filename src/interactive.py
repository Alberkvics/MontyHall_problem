"""
interactive.py - Interactive mode: the user plays one round at time
"""

import random
from src.game import setup_game, host_opens, resolve_game, GameState
from src.bayes import bayesian_update
from src.display import (C, show_doors, show_bayesian_update, show_game_result, show_separator)


def _ask_int(prompt: str, valid: list[int]) -> int:
    """
    Reads a valid integer from the user with error handling
    """
    while True:
        try:
            val = int(input(prompt).strip())
            if val in valid:
                return val
            print(C.red(f"Please choose one of: {valid}"))
        except (ValueError, EOFError):
            print(C.red("Invalid input. Try again"))


def _ask_yes_no(prompt: str) -> bool:
    while True:
        ans = input(prompt).strip().lower()
        if ans in (""):
            return True
        if ans in ("y", "yes", "1"):
            return True
        if ans in ("n", "no", "0"):
            return False
        print(C.red("Type y (yes) or n (no)"))


def play_interactive(n_doors: int = 3):
    """
    Runs a complete interactive round
    """
    rng = random.Random()

    print()
    show_separator("=")
    print(C.bold(C.cyan("Interactive Mode")))
    show_separator("=")

    ## PHASE ONE: INITIAL CHOICE
    print(f"\n  There are {n_doors} doors. Behind one of them is a 🚗  car.")
    print(f"  Behind the others: 🐐  goats. Good luck!\n")

    door_states = {d: "closed" for d in range(1, n_doors + 1)}
    show_doors(n_doors, door_states)

    car_door    = setup_game(n_doors, rng)
    valid_doors = list(range(1, n_doors + 1))

    player_choice = _ask_int(
        f"\n  {C.bold('Pick a door')} ({', '.join(map(str, valid_doors))}): ",
        valid_doors
    )

    door_states[player_choice] = "chosen"
    print(f"\n  You chose door {C.cyan(str(player_choice))}.\n")
    show_doors(n_doors, door_states)

    ## PHASE TWO: MONTY ACTS
    host_reveal = host_opens(n_doors, car_door, player_choice, rng)
    door_states[host_reveal] = "revealed"

    print(f"\n  {C.bold(C.magenta('Monty Hall'))} opens door "
          f"{C.red(str(host_reveal))} revealing a 🐐  goat!\n")
    show_doors(n_doors, door_states)

    ## PHASE THREE BAYESIAN DERIVATION
    print(f"\n  {C.dim('Computing what Bayes says about your chances...')}")
    upd = bayesian_update(n_doors, player_choice, host_reveal)
    show_bayesian_update(upd)

    ## PHASE FOUR: FINAL DECISION
    remaining = [
        d for d in range(1, n_doors + 1)
        if d != player_choice and d != host_reveal
    ]

    print(C.bold(f"\n  DECISION TIME"))
    print(f"  Your current door : {C.cyan(str(player_choice))}")
    print(f"  Available door(s) : {C.yellow(str(remaining[0]) if len(remaining) == 1 else str(remaining))}")

    switch = _ask_yes_no(
        f"\n  {C.bold('Do you want to switch doors?')} (Y/N): "
    )

    final_choice, won = resolve_game(n_doors, car_door, player_choice,
                                     host_reveal, switch, rng)

    state = GameState(
        n_doors=n_doors,
        car_door=car_door,
        player_choice=player_choice,
        host_reveal=host_reveal,
        final_choice=final_choice,
        switched=switch,
        won=won,)

    show_game_result(state)

    return _ask_yes_no("  Play another round? (Y/N): ")
