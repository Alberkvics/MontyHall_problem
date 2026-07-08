"""
bayes.py - Full Bayesian derivation

Notation:
    C_i = Car is behind door i
    H_i = Monty opens door j

Bayes' Theorem:
    P(C_i | H_j) = P(H_j | C_i) * P(C_i) / P(H_j)

Where:
    P(C_i)        = prior (belief before Monty acts)
    P(H_j | C_i)  = likelihood (prob. of Monty opening j, given car is at i)
    P(H_j)        = evidence (normalizer)
    P(C_i | H_j)  = posterior (updated belief)
"""

from fractions import Fraction
from dataclasses import dataclass


@dataclass
class BayesianUpdate:
    """
    Complete result of Bayesian Update
    """
    n_doors: int
    player_choice: int
    host_reveal: int
    car_door_hypotheses: list[int] # ALL POSSIBLES

    priors: dict[int, Fraction]
    likelihoods: dict[int, Fraction]
    unnormalized: dict[int, Fraction]
    evidence: Fraction
    posteriors: dict[int, Fraction]

    @property
    def posterior_stay(self) -> Fraction:
        return self.posteriors[self.player_choice]
    
    @property
    def posterior_switch(self) -> Fraction:
        """
        Probability of winning by switching == sum of posteriors for doors
        that are neither the player's choice or the revealed one
        """
        switch_doors = [
            d for d in self.car_door_hypotheses
            if d != self.player_choice and d != self.host_reveal
        ]
        return sum(self.posteriors[d] for d in switch_doors)


def compute_likelihood(door_hypothesis: int,
                       host_reveal: int,
                       player_choice: int,
                       n_doors: int) -> Fraction:
    """
    P(H_j | C_i) -> Probability of Monty opening door j,
    given that the car is behind door i
    
    Rules:
    Monty NEVER opens the player's door
    Monty NEVER reveals the car
    If multiple valid options exist, Monty chooses uniformly
    
    Cases:
    1. host_reveal == player_choice -> IMPOSSIBLE
    2. host_reveal == door_hypothesis -> IMPOSSIBLE
    3. door_hypothesis == player_choice -> Monty has (n_doors - 1) valid options
                                        -> likelihood == 1 / (n_doors - 1)
    4. door_hypothesis != player_choice and != host_reveal -> Monty was forced to open host_reveal
                                                            -> likelihood = 1
    """
    if host_reveal == player_choice:
        return Fraction(0)
    if host_reveal == door_hypothesis:
        return Fraction(0)
    if door_hypothesis == player_choice:
        # CAR IS AT THE PLAYER'S DOOR, MONTY CAN OPEN ANY DOOR (n - 1)
        return Fraction(1, n_doors - 1)
    else:
        # CAR IS AT ANOTHER DOOR (NOT player_choice, NOT host_reveal):
        # MONTY IS FORCED TO OPEN EXACTLY host_reveal -> prob = 1
        return Fraction(1)


def bayesian_update(n_doors: int,
                    player_choice: int,
                    host_reveal: int) -> BayesianUpdate:
    """
    Performs the full Bayesian Update for a Monty Hall round
    uniform prior: P(C_i) = 1 / n_doors for all i
    """
    doors = list(range(1, n_doors + 1))
    prior = Fraction(1, n_doors)

    priors = {d: prior for d in doors}

    likelihoods = {
        d: compute_likelihood(d, host_reveal, player_choice, n_doors)
        for d in doors
    }

    unnormalized = {
        d: priors[d] * likelihoods[d]
        for d in doors
    }

    evidence = sum(unnormalized.values())

    posteriors = {
        d: unnormalized[d] / evidence
        for d in doors
    }

    return BayesianUpdate(
        n_doors=n_doors,
        player_choice=player_choice,
        host_reveal=host_reveal,
        car_door_hypotheses=doors,
        priors=priors,
        likelihoods=likelihoods,
        unnormalized=unnormalized,
        evidence=evidence,
        posteriors=posteriors,)
