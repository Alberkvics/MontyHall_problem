"""
game.py - Core logic for the Monty Hall Problem
"""

import random
from dataclasses import dataclass


@dataclass
class GameState:
    """ 
    Representes the complete state os one round
    """
    n_doors: int # THREE
    car_door: int # DOOR HIDING THE PRIZE
    player_choice: int # PLAYER'S INITIAL DOOR
    host_reveal: int # DOOR OPENED BY MONTY (GOAT/LIKELIHOOD)
    final_choice: int # PLAYER'S FINAL DOOR
    switched: bool # SWITCHED OR NOT?
    won: bool      # THAT'S THE QUESTION


def setup_game(n_doors: int = 3, rng: random.Random = None) -> int:
    """
    Randomly places the car ans returns its door number
    Separated to allow testing and reproducibility
    
    Returns:
        car_door: int -> door hiding the prize
    """

    rng = rng or random
    return rng.randint(1, n_doors)


def host_opens(n_doors: int,
               car_door: int,
               player_choice: int,
               rng: random.Random = None) -> int:
    """
    Monty Hall opens one door that:
        is not the player's choice
        does not hide the prize"
    
    If multiple valid doors exist, Monty picks at random
    (important for the Bayesin derivation)

    Returns:
        door: int -> the door Monty reveals
    """

    rng = rng or random
    available = [
        d for d in range(1, n_doors +1)
        if d != player_choice and d != car_door
    ]
    return rng.choice(available)


def resolve_game(n_doors: int,
                 car_door: int,
                 player_choice: int,
                 host_reveal: int,
                 switch: bool,
                 rng: random.Random = None) -> tuple[int, bool]:
    """
    Given wheter the player switches, returns -> final choice and won
    
    If switch = T, the player pickes randomly among remaining doors
    (excluding ther current choice and door opendes by Monty)
    """
    rng = rng or random
    if switch:
        remaining = [
            d for d in range(1, n_doors + 1)
            if d != player_choice and d != host_reveal
        ]
        final_choice = rng. choice(remaining) # THREE DOORS, ONE OPTION
    else:
        final_choice = player_choice

    won = (final_choice == car_door)
    return final_choice, won


def play_one_game(n_doors: int,
                    player_choice: int = None,
                    switch: bool = None,
                    rng: random.Random = None) -> GameState:
    """
    Simulates a complete round.
    Automatic Simulation
    player_choice and switch can be random (None) or fixed
    """
    rng = rng or random
    car_door = setup_game(n_doors, rng)
    if player_choice is None:
        player_choice = rng.randint(1, n_doors)
    if switch is None:
        switch = rng.choice({True, False})

    host_reveal = host_opens(n_doors, car_door, player_choice, rng)
    final_choice, won = resolve_game(n_doors, car_door, player_choice,
                                     host_reveal, switch, rng)
    
    return GameState(n_doors=n_doors, # ARGUMENT
                     car_door=car_door,
                     player_choice=player_choice,
                     host_reveal=host_reveal,
                     final_choice=final_choice,
                     switched=switch,
                     won=won,
                     )
