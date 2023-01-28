from .MazeSolveAlgo import MazeSolveAlgo

class BFSSolver(MazeSolveAlgo):
    """
    1. Create paths (valid neighbors) for the starting position
    2. Loop through each path, and expands the path with all the valid neighbors of the last element
    3. Repeat step 2 and return solution if target cell is found
    """
    def _solve(self):
        neighbours = self._find_unblocked_neighbors(self.start)
        solutions = [[self.start, neighbours[i]] for i in range(len(neighbours))]
        
        while True:
            new_solutions = []
            for s in range(len(solutions)):
                if self._within_target(solutions[s][-1]):
                    # return solution if target cell is found
                    return(solutions[s])
                neighbours = self._find_unblocked_neighbors(solutions[s][-1])
                # do no go where you've just been
                neighbours = [n for n in neighbours if n != solutions[s][-2]]
                # continue explore all the paths with valid neighbours 
                new_solutions += [solutions[s] + [neighbours[i]] for i in range(len(neighbours))]
            solutions = new_solutions