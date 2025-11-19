class PathFinder:
    def __init__(self, graph_edges):
        self.graph = graph_edges

    def neighbors(self, node):
        return self.graph.get(node, [])

    def estimate_to_goal(self, node, goal):
        # Simple admissible heuristic: 
        # Since we don't have coordinates, we use a lookup table.
        # In real applications, this could be Euclidean/Manhattan distance.
        heuristic_table = {
            'A': 8,
            'B': 5,
            'C': 3,
            'D': 0
        }
        return heuristic_table.get(node, float('inf'))

    def find_shortest_path(self, start, target):
        frontier = {start}
        explored = set()

        cost_so_far = {start: 0}
        previous_node = {start: None}

        while frontier:
            current = min(frontier, key=lambda n: cost_so_far[n] + self.estimate_to_goal(n, target))

            if current == target:
                path = []
                step = current
                while step is not None:
                    path.append(step)
                    step = previous_node[step]
                return list(reversed(path))

            frontier.remove(current)
            explored.add(current)

            # Check all neighbors
            for neighbor, edge_cost in self.neighbors(current):
                if neighbor in explored:
                    continue

                new_cost = cost_so_far[current] + edge_cost

                # If neighbor is new or we found a better path
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    previous_node[neighbor] = current
                    frontier.add(neighbor)

        return None  # No path exists


# ------------------ Lab Test Case ------------------
if __name__ == "__main__":
    edges = {
        'A': [('B', 1), ('C', 3), ('D', 7)],
        'B': [('D', 5)],
        'C': [('D', 12)]
    }

    solver = PathFinder(edges)
    result = solver.find_shortest_path('A', 'D')

    if result:
        print("Shortest path found:", " → ".join(result))
    else:
        print("No valid path exists from start to goal.")