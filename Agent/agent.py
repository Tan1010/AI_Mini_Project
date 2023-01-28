from .bfs import BFSSolver
from .backtracking import BacktrackingSolver

def agent(method='backtracking'):
    if method == 'backtracking':
        return BacktrackingSolver()
    if method == 'bfs':
        return BFSSolver()
    return None
