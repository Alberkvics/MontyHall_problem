"""
main.py - Entry point for the Monty_Hall Problem simulator

Usage:
    python main.py

Project Structure:
    main.py - Loop and Menu
    src/
    ├── bayes.py - Full Bayesian derivation
    ├── display.py - All Visual Output
    ├── game.py - Game Logic
    ├── interactive.py - Interactive Game Mode
    └── simulation.py - Automatic Simulation Mode
"""

import sys
from src.display import show_title, show_menu, C
from src.interactive import  play_interactive
from src.simulation import run_simulation, ask_simulation_params


def main():
    show_title()

    while True:
        show_menu()
        try:
            choice = input("Option:").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n    {C.dim("Goodbye! 👋")}\n")
            sys.exit(0)
    
        if choice == "0":
            print(f"\n    {C.dim("See you next time! 👋")}\n")
            break

        elif choice == "1":
            play_again = True
            while play_again:
                play_again = play_interactive(n_doors=3)
        
        elif choice == "2":
            n_games, verbose = ask_simulation_params()
            run_simulation(n_games=n_games, verbose=verbose)

        else:
            print(C.red("Invalid option. Please try again"))


if __name__ == "__main__":
    main()