#/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt

# Computes the expected score of a (dice) game of Pig if your strategy is
# to stop rolling if you hit a score greater than or equal to `target`.
def expected_pig_score(target):
    # First we build a transition markov matrix for the game, given our
    # strategy.  The maximum score we can get is target + 5.  We start at zero.
    # The last state represents death (if we rolled a one).
    num_states = target + 7 
    death_state = target + 6

    transitions = np.zeros([num_states, num_states])
    for i in range(0, target):
        # If we're below the target, we roll, in which case we might...
        transitions[i,death_state] = 1/6 # Roll a one, and go to the death state.
        for x in range(2, 7):
            transitions[i,i+x] = 1/6  # Roll a 2-6 and gain that many points.
    for i in range(target, num_states):
        transitions[i,i] = 1
        # If we're at or above the target (or dead) we stay put (absorbing state)

    transitions = np.linalg.matrix_power(transitions, target)
    # By raising the matrix to a power, we ask what would happen if we
    # attempted to step the game `target` times.  Since the game knows how to
    # stay put once it finishes, and it takes less than `target` steps to
    # finish, we now have a transition matrix for how the game ends.

    outcome_probabilities = transitions[0]
    # We started at state 0 (alive, with no points) so this is the row of the
    # matrix that tells us how likely the game is to terminate.

    outcome_values = np.concatenate([np.arange(target+6), [0]])
    # Each state is worth the same as its index (how many points we got to)
    # except for the death state which is worth 0 despite being at the end.

    return np.dot(outcome_probabilities, outcome_values)
    # E[score] = sum_s(probability*s)


# Now let's plot the first 50 of them in a nice little graph:
N = 50
xs = np.arange(N)
scores = [expected_pig_score(n) for n in xs]
plt.title('Expected Scores in Pig')
plt.xlabel('Target Score')
plt.ylabel('Expected Score')
plt.plot(xs, scores)
plt.show()

