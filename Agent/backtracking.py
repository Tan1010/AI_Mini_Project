from random import choice
from .MazeSolveAlgo import MazeSolveAlgo

class BacktrackingSolver(MazeSolveAlgo):
    """
    1. Pick a random direction and follow it until the target cell (sugar/home) is reached
    2. Backtrack if and only if you hit a dead end/visited cells.
    """
    def _solve(self):
        solution = []
        solution.append(self.start)

        # pick a random neighbor and travel to it, until you're at the target cell
        while not self._within_target(solution[-1]):
            neighbours = self._find_unblocked_neighbors(solution[-1])
            # do no go where you've just been
            if len(neighbours) > 1 and len(solution) > 1:
                if solution[-2] in neighbours:
                    neighbours.remove(solution[-2])
            next = choice(neighbours)
            solution.append(next)
        return solution