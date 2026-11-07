"""Mission 1 starter, created in student_submission/mission_1/planners.py.

Open that submission file in your editor and implement the four functions.
The guide creates it automatically and never overwrites an existing file.

Each function receives ctx with start, goal, grid, heuristic(cell) and
expand(cell, frontier_size). Return a list of (row, column) cells including
start and goal, or [] after exhausting the search. Call ctx.expand once per
expanded node. Record the actual frontier size, not the number of visited cells.
The runner enforces an expansion budget and a separate process time limit.
Use only the Python standard library. Do not import planning.reference_path.
When a free start is already the goal, return the single starting cell with
zero moves. No expansion is required for that case. Use the six small checks
on the Mission 1 page before running the full canonical-map evaluation.
"""
from collections import deque
from heapq import heappush, heappop
from planning.core import reconstruct




#HELPER: rebuild path from a parent dictionary
def _path(parents, goal):
    path = []
    cell = goal
    while cell is not None:
        path.append(cell)
        cell = parents[cell]
    path.reverse()
    return path


def bfs(ctx):
    """FIFO queue. Mark discovered cells when enqueuing and store parents.
    Use ctx.expand(current, len(frontier)+1) to obtain neighbours.
    BFS minimizes number of unit-cost edges, not execution time on a robot.
    """
    start, goal = ctx.start, ctx.goal

    #free start that is already the goal
    if start == goal:
        return [start]

    frontier = deque([start])
    parents = {start: None} #doubles as the discovered set

    while frontier:
        current = frontier.popleft()

        #goal test when node is removed from the queue
        if current == goal:
            return _path(parents, goal)

        #expand once
        for neighbor in ctx.expand(current, len(frontier) + 1):
            if neighbor not in parents:
                parents[neighbor] = current
                frontier.append(neighbor)

    return [] #returns empty list if not path was found

def dfs(ctx):
    """LIFO stack. Track discovered cells and parents to avoid cycles.
    A valid DFS path need not be shortest. Keep the supplied neighbour order.
    """
    start, goal = ctx.start, ctx.goal

    if start == goal:
        return [start]

    stack = [(start, None)]  # (cell, parent)
    parents = {} #tracks cells that have been visited

    while stack:
        current, parent = stack.pop()
        
        if current in parents:
            continue  # already visited

        parents[current] = parent

        if current == goal:
            return _path(parents, goal)

        neighbors = ctx.expand(current, len(stack) + 1)

        for neighbor in reversed(list(neighbors)):  # reverse to maintain order when popping from stack
            if neighbor not in parents:
                stack.append((neighbor, current))

    return []  # returns empty list if no path was found


def iddfs(ctx):
    """Run depth-limited DFS with bounds 0, 1, 2, ... .
    Prevent cycles on the current path. Do not keep a global visited set across
    depth limits. Count expansions again on every iteration. Return [] only
    after exhaustive failure. Catch no budget exceptions. The runner records
    resource_limit honestly if this expensive method reaches its budget.
    """

    start, goal = ctx.start, ctx.goal

    if start == goal:
        return [start]

    limit = 0
    while True:
        # Fresh state every iteration (no global visited set)
        path = [start]
        on_path = {start}
        cutoff = False               # True if the limit hid deeper cells

        # Each frame is an iterator over the neighbors of path[i]
        # (expanded only if we are below the depth limit)
        if limit > 0:
            frames = [iter(ctx.expand(start, 1))]
        else:
            frames = [iter(())]
            cutoff = True            # start has cells beyond limit 0

        while frames:
            nxt = next(frames[-1], None)

            # Out of neighbors: backtrack
            if nxt is None:
                frames.pop()
                on_path.discard(path.pop())
                continue

            # Cycle prevention on the current path only
            if nxt in on_path:
                continue

            path.append(nxt)
            on_path.add(nxt)

            if nxt == goal:
                return path

            depth = len(path) - 1
            if depth < limit:
                frames.append(iter(ctx.expand(nxt, len(path))))
            else:
                cutoff = True        # at the limit, cannot go deeper
                frames.append(iter(()))

        # No cutoff means the whole reachable space was searched
        if not cutoff:
            return []
        limit += 1


def astar(ctx):
    """Use a heap ordered by g + ctx.heuristic(cell).
    Keep best g costs and parents. Ignore outdated heap entries. Each edge
    costs 1. Stop when the goal is removed from the priority queue.
    """
    start, goal = ctx.start, ctx.goal

    if start == goal:
        return [start]

    counter = 0                      # tie-breaker so cells are never compared
    heap = [(ctx.heuristic(start), counter, 0, start)]   # (f, count, g, cell)
    best_g = {start: 0}
    parents = {start: None}

    while heap:
        f, _, g, current = heappop(heap)

        # Ignore outdated heap entries
        if g > best_g[current]:
            continue

        # Stop when the goal is REMOVED from the queue
        if current == goal:
            return _path(parents, goal)

        for nb in ctx.expand(current, len(heap) + 1):
            new_g = g + 1            # every edge costs 1
            if new_g < best_g.get(nb, float('inf')):
                best_g[nb] = new_g
                parents[nb] = current
                counter += 1
                heappush(heap, (new_g + ctx.heuristic(nb), counter, new_g, nb))

    return []