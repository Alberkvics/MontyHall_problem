# MontyHall_problem

This is a simple Python program, written with no external dependencies, to help you learn and understand Bayesian inference through the famous Monty Hall problem.

It allows you to play interactively by choosing a door and deciding whether to switch after one losing door is revealed. You can also simulate `n` games to observe the statistical behavior over a large number of trials.

```math
P(\theta \mid D) = \frac{P(D \mid \theta) P(\theta)}{P(D)}
```
Where:

$\theta$ is the parameter non observed;

$D$ is my evidence, the data;

$P (\theta \mid D)$ is the *posteriori* distribution and the output of Bayesin Equation;

$P(D \mid \theta)$ 
is the likelihood, and it plays a crucial role in Bayesian inference because it tells us how new observations update our beliefs about $\theta$.
In the Monty Hall problem, the new data $D$ corresponds to the door opened by Monty. This is an additional piece of information that reveals what is behind one of the other doors and changes the initial winning probability of $1 / 3$. After Monty opens a door that does not contain the prize, the probability of winning by switching becomes $2 / 3$.
The key idea is that Monty cannot open your chosen door, or not the door that has the prize. His action of opening a losing door is therefore informative, and this information is captured by the likelihood term 
$P(D \mid \theta)$.
If we extend this intuition to a scenario with many doors, for example 100 (one hundred) doors, Monty will open 98 (ninty eight) losing doors, leaving only your original choice and one remaining unopened door. In this situation, almost all the probability mass shifts to the other unopened door, illustrating how the likelihood incorporates new evidence and strongly favors switching;

$P(\theta)$ is the *prior* distribution.

NOTES

1. Explanation under construction



---
<p align="center">
Made by &nbsp;·&nbsp; André Alberkovics</a>
</p>