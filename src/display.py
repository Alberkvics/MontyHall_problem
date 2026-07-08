"""
display.py - Visual Output
"""

from fractions import Fraction
from src.bayes import BayesianUpdate
from src.game import GameState


## ANSI Colors

class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_DARK = "\033[40m"

    # MAKING LIFE A LITTLE EASIER
    @staticmethod
    def bold(s): return f"{C.BOLD}{s}{C.RESET}"
    @staticmethod
    def green(s): return f"{C.GREEN}{s}{C.RESET}"
    @staticmethod
    def red(s): return f"{C.RED}{s}{C.RESET}"
    @staticmethod
    def yellow(s): return f"{C.YELLOW}{s}{C.RESET}"
    @staticmethod
    def cyan(s): return f"{C.CYAN}{s}{C.RESET}"
    @staticmethod
    def magenta(s): return f"{C.MAGENTA}{s}{C.RESET}"
    @staticmethod
    def dim(s): return f"{C.DIM}{s}{C.RESET}"


## Graphic Elements

def door_icon(door_num: int, state: str = "closed") -> str:
    """
    state: 'closed', 'car', 'goat', 'chosen', 'revealed'
    """
    icons = { # MAKING THE DOORs GRAPHICS
        "closed": f"┌───┐\n│ {C.cyan(str(door_num))} │\n│   │\n└───┘",
        "car": f"┌───┐\n│ {C.cyan(str(door_num))} │\n│{C.yellow('🚗')} │\n└───┘",
        "goat": f"┌───┐\n│ {C.cyan(str(door_num))} │\n│{C.dim('🐐')} │\n└───┘",
        "chosen": f"┌───┐\n│ {C.cyan(str(door_num))} │\n│{C.green(' ✓')} │\n└───┘",
        "revealed": f"┌───┐\n│ {C.red(str(door_num))} │\n│{C.dim('🐐')} │\n└───┘" ## NO COMMA, LET'S TEST
    }
    return icons.get(state, icons["closed"])


def show_doors(n_doors: int, states: dict[int, str]):
    """
    Print Doors
    """
    door_lines = []
    for d in range(1, n_doors +1):
        state = states.get(d, "closed")
        lines = door_icon(d, state).split("\n")
        door_lines.append(lines)
    
    for row in range(len(door_lines[0])):
        print("  ".join(col[row] for col in door_lines))


def show_separator(char="-", width=60, color=C.DIM):
    print(f"{color}{char * width}{C.RESET}")


def show_title():
    print()
    print(C.bold(C.cyan("____________________________________________")))
    print(C.bold(C.cyan("____________________________________________")))
    print(C.bold(C.cyan("____________________________________________")))
    print(C.bold(C.cyan("___________THE MONTY HALL PROBLEM___________")))
    print(C.bold(C.cyan("____________________________________________")))
    print(C.bold(C.cyan("____________________________________________")))
    print(C.bold(C.cyan("____________________________________________")))
    print()


def show_menu():
    print(C.bold("\nWhat would you like to do?"))
    print(f"  {C.cyan('[1]')} - Play the game interactively")
    print(f"  {C.cyan('[2]')} - Run a simulation")
    print(f"  {C.cyan('[0]')} - Quit")
    print()


## BAYESIAN DISPLAY

def _fmt_fraction(f: Fraction, width: int = 6) -> str:
    """
    Four-decimal float, right aligned
    """
    return f"{float(f):.4f}".rjust(width)

def _fraction_bar(f: Fraction, width: int = 20) -> str:
    """
    Progess bar
    """
    filled = round(float(f) * width)
    bar = "█" * filled + "░" * (width - filled)
    return bar

def show_bayesian_update(upd: BayesianUpdate):
    """
    Full Bayesian Update Table
    door | prior | likelihood | prior x likelihood | posterior
    """
    print()
    show_separator()
    print(C.bold(C.magenta("Bayesian Update Table")))
    show_separator()

    print(C.dim(
        "\n Bayes Theorem: P(A|B) = P(B|A) * P(A) / P(B)\n"
        f"  Where B = Monty opened door {upd.host_reveal}\n"
    ))

    ## HEADER
    header = (
        f"  {'Door':^6} | {'Prior':^6} | {'Likelihood':^12} |" # ^6 FOR CENTRALIZE THE TEXT IN SIX SPACES
        f"{'Prior X Likelihood':^20} | {'Posterior':^10} | {'Bar':^20}"
    )
    print(C.bold(header))
    #

    for d in upd.car_door_hypotheses:
        prior = upd.priors[d]
        lik = upd.likelihoods[d]
        unnorm = upd.unnormalized[d]
        post = upd.posteriors[d]

        # HIGHLIGHT RELEVANT DOORS
        if d == upd.player_choice:
            label = C.green(f"{d:^6}")
            tag = C.green(" <- your door")
        elif d == upd.host_reveal:
            label = C.red(f"{d:^6}")
            tag = C.red(" <- Monty's door")
        else:
            label = C.yellow(f"{d:^6}")
            tag = C.yellow(" <- switch to?")
        
        bar = _fraction_bar(post, 20)

        ## LIKELIHOOD AS READABLE FRACTION
        if lik == 0:
            lik_str = "0"
        elif lik.denominator == 1:
            lik_str = f"1"
        else:
            lik_str = f"1/{lik.denominator:<7}"

        print(
            f"{label} | {_fmt_fraction(prior):^8} | {lik_str:^14} |"
            f"{_fmt_fraction(unnorm):^8} | {_fmt_fraction(post):^10} | {bar}"
            f"{tag}"
        )

    print()
    print(f"    {C.dim('Evidence P(B):')} {float(upd.evidence):.4f}")
    print()

    ## FINAL SUMMARY
    stay_p = float(upd.posterior_stay)
    switch_p = float(upd.posterior_switch)

    print(C.bold("CONCLUSION:"))
    print(
        f"  Keep door {upd.player_choice}:  "
        f"  {C.green(f'{stay_p:.4f}')}  ({Fraction(stay_p).limit_denominator(10)})")
    print(
        f"  Switch door:  "
        f"  {C.yellow(f'{switch_p:.4f}')}  ({Fraction(switch_p).limit_denominator(10)})")
    
    better = "SWITCH" if switch_p > stay_p else "STAY"
    ratio = switch_p / stay_p if stay_p > 0 else float("inf")
    print(
        f"\n -> {C.bold(C.cyan(f'Optimal strategy: {better}'))}"
        f"{C.dim(f'(switching is {ratio:.1f} X more advantageous)')}")
    show_separator()

## GAME RESULT

def show_game_result(state: GameState):
    """
    Final results, with all doors opened
    """
    print()
    print(C.bold("Final Result - opening all doors:"))
    print()

    door_states = {}
    for d in range(1, state.n_doors +1):
        if d == state.host_reveal:
            door_states[d] = "revealed"
        elif d == state.car_door:
            door_states[d] = "car"
        else: door_states[d] = "goat"

    show_doors(state.n_doors, door_states)
    print()

    action = "Switched" if state.switched else "Stayed"
    print(f" Initial choice: door {C.cyan(str(state.player_choice))}")
    print(f" Monty opened: door {C.red(str(state.host_reveal))} (goat)")
    print(f" Action : {C.bold(action)} -> door {C.cyan(str(state.final_choice))}")
    print(f" Car was behind: door {C.yellow(str(state.car_door))}")
    print()

    if state.won:
        print(C.bold(C.green(" YOU WON THE CAR!")))
    else:
        print(C.bold(C.red("YOU WON.....A GOAT")))
    print()


## Simulation 

def show_simulation_results(n_games: int,
                            n_doors: int,
                            wins_switch: int,
                            wins_stay: int,
                            losses_switch: int,
                            losses_stay: int):
    """
    Statistics
    """
    games_switch = wins_switch + losses_switch
    games_stay = wins_stay + losses_stay

    rate_switch = wins_switch / games_switch if games_switch else 0
    rate_stay = wins_stay / games_stay if games_stay else 0

    # THEORICAL VALUES DERIVED FROM n_doors
    teoria_switch = 1 - (1 / n_doors)
    teoria_stay = 1 / n_doors

    print()
    show_separator("=")
    print(C.bold(C.cyan(f" Results = {n_games} games simulated")))
    show_separator("=")

    print(C.bold("\n Strategy: Always Switch"))
    _show_bar_stat("Wins", wins_switch, games_switch, C.GREEN)
    _show_bar_stat("Losses", losses_switch, games_switch, C.RED)
    print(f"Win Rate: {C.bold(C.green(f'{rate_switch:.2%}'))}"
          f"{C.dim(f'(theory: {teoria_stay:.2%})')}")
     
    print(C.bold("\n Strategy: Never Switch"))
    _show_bar_stat("Wins", wins_stay, games_stay, C.GREEN)
    _show_bar_stat("Losses", losses_stay, games_stay, C.RED)
    print(f"Win Rate: {C.bold(C.red(f'{rate_stay:.2%}'))}"
           f"{C.dim(f'(theory: {teoria_stay:.2%})')}")
    
    print()
    print(C.dim("As N -> infinite, the rates converge to the theorical values"))
    show_separator("=")
    print()

def _show_bar_stat(label: str,
                   count: int,
                   total: int,
                   color: str):
    if total == 0:
        return
    ratio = count / total
    filled = round(ratio * 30)
    bar = f"{color}{'█' * filled}{C.DIM}{'░' * (30 - filled)}{C.RESET}"
    print(f"{label:<10} {bar} {count:>6} / {total} ({ratio:.1%})")

