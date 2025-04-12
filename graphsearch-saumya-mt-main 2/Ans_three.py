import networkx as nx
import matplotlib.pyplot as plt
from queue import PriorityQueue



def create_example_graph():
    G = nx.Graph()
    # Add nodes
    G.add_nodes_from(['A', 'B', 'C', 'D', 'E', 'F', 'G'])

    # Add weighted edges
    edges = [
        ('A', 'B', 2),
        ('A', 'C', 1),
        ('B', 'D', 10),
        ('C', 'E', 2),
        ('D', 'G', 2),
        ('E', 'F', 5),
        ('F', 'G', 1)
    ]
    G.add_weighted_edges_from(edges)

    # Misleading heuristic values for Greedy Search
    heuristic = {
        'A': 6,
        'B': 1,  # Low value encourages Greedy to go to B
        'C': 5,
        'D': 0,  # Makes D seem closer to the goal
        'E': 4,
        'F': 3,
        'G': 0  # Goal
    }
    return G, heuristic

def greedy_search(G, source, target, heuristic):
    """
    Perform Greedy search using the heuristic to expand nodes.
    Returns the path found.
    """
    open_set = PriorityQueue()
    open_set.put((heuristic[source], [source]))  # (heuristic value, path)

    while not open_set.empty():
        _, path = open_set.get()
        node = path[-1]

        if node == target:
            return path

        for neighbor in G.neighbors(node):
            if neighbor not in path:  # Avoid cycles
                new_path = path + [neighbor]
                open_set.put((heuristic[neighbor], new_path))

    return []

def uniform_cost_search(G, source, target):
    """
    Perform Uniform Cost Search to find the shortest path based on edge weights.
    Returns the path found and the total cost.
    """
    open_set = PriorityQueue()
    open_set.put((0, [source]))  # (cumulative cost, path)
    g_costs = {source: 0}

    while not open_set.empty():
        current_cost, path = open_set.get()
        node = path[-1]

        if node == target:
            return path, current_cost

        for neighbor in G.neighbors(node):
            edge_weight = G.edges[node, neighbor]['weight']
            new_cost = current_cost + edge_weight

            if neighbor not in g_costs or new_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_cost
                new_path = path + [neighbor]
                open_set.put((new_cost, new_path))

    return [], float('inf')

def visualize_search(G, path, search_name):
    """
    Visualize the graph with the path highlighted.
    """
    pos = nx.spring_layout(G, seed=42)
    colors = ['red' if (u, v) in zip(path, path[1:]) or (v, u) in zip(path, path[1:]) else 'gray' for u, v in G.edges()]

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color=colors, node_size=700, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Add title
    plt.title(f"{search_name} Path: {' -> '.join(path)}")
    plt.tight_layout()
    plt.savefig(f"three{search_name.lower().replace(' ', '_')}_result.png")
    plt.close()

def main():
    G, heuristic = create_example_graph()

    # Perform Greedy Search with the heuristic
    greedy_path = greedy_search(G, 'A', 'G', heuristic)
    visualize_search(G, greedy_path, 'Greedy Search (Misleading Heuristic)')

    # Perform Uniform Cost Search
    ucs_path, ucs_cost = uniform_cost_search(G, 'A', 'G')
    visualize_search(G, ucs_path, 'Uniform Cost Search (Optimal Path)')

# Run the main function
main()
"""
Analysis:
Greedy Search may choose A -> B -> D -> G, thinking it's the best path based on the heuristic. However, the actual cost is 2 + 10 + 2 = 14.
BFS or UCS would find the optimal path as A -> C -> E -> F -> G with a total cost of 1 + 2 + 5 + 1 = 9.
"""