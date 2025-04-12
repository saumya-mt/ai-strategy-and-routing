import csv
import math
import matplotlib.pyplot as plt
import networkx as nx
from queue import PriorityQueue

"""
This program implements graph search algorithms including BFS, DFS, and A* on a weighted graph.
It also visualizes the search paths for each algorithm using NetworkX and Matplotlib.
The graph data is loaded from CSV files containing node coordinates and edges with weights.
@author [Saumya Mishra]
"""

def load_positions_from_file(fileName):
    """
    Load node positions (coordinates) from a CSV file and return them as a dictionary.
    The file should have the following format: Node, x-axis, y-axis.
    """
    positions = {}
    with open(fileName, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            Nodes, xaxis, yaxis = row
            positions[Nodes] = (int(xaxis), int(yaxis))
    return positions

def load_edges_from_file(fileName):
    """
    Load edges with weights from a CSV file and return a NetworkX graph.
    The file should have the following format: Neighborhood1, Neighborhood2, Weight.
    """
    G = nx.Graph()
    with open(fileName, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            Neighborhood1, Neighborhood2, Weight = row
            G.add_edge(Neighborhood1, Neighborhood2, Weight=int(Weight))

    print("Nodes in graph:", G.nodes())
    print("Edges in graph:", G.edges(data=True))
    return G

def mybfs(G, source, target):
    """
    Perform Breadth-First Search (BFS) on the graph to find the shortest path from source to target.
    Return a tuple containing a list of expanded edges and a list of edges in the final path.
    """
    visited = {source}
    queue = [[source]]
    expanded_edges = []

    if source == target:
        return [], []

    while queue:
        path = queue.pop(0)
        node = path[-1]

        # Sort neighbors lexicographically
        for neighbor in sorted(G.neighbors(node)):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                expanded_edges.append((node, neighbor))

                if neighbor == target:
                    # Generate the final path as a list of edges
                    final_path = [(new_path[i], new_path[i + 1]) for i in range(len(new_path) - 1)]
                    return expanded_edges, final_path

    return expanded_edges, []

def mydfs(G, source, target):
    """
    Perform Depth-First Search (DFS) to find the lexicographically smallest path from source to target.
    Return a tuple containing a list of expanded edges and a list of edges in the final path.
    """
    stack = [[source]]  # Stack contains paths
    visited = set()
    expanded_edges = []
    lex_smallest_path = None

    while stack:
        # Pop the last path from the stack
        path = stack.pop()
        node = path[-1]

        # If we have reached the target
        if node == target:
            # Update the lex smallest path if necessary
            if lex_smallest_path is None or path < lex_smallest_path:
                lex_smallest_path = path
            continue  # Continue to find if there's a lex smaller path

        if node not in visited:
            visited.add(node)

            # Get neighbors sorted in lex order
            neighbors = sorted(G.neighbors(node))

            # Push neighbors onto the stack to continue DFS
            for neighbor in reversed(neighbors):  # Reverse to maintain lex order in stack
                if neighbor not in path:  # Avoid cycles
                    new_path = path + [neighbor]
                    stack.append(new_path)
                    expanded_edges.append((node, neighbor))

    # If a path was found, construct the final path edges
    if lex_smallest_path:
        final_path_edges = [(lex_smallest_path[i], lex_smallest_path[i + 1]) for i in range(len(lex_smallest_path) - 1)]
        return expanded_edges, final_path_edges
    else:
        return expanded_edges, []

def euclidean_distance(pos1, pos2):
    """
    Calculate the Euclidean distance between two points.
    """
    return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def myastar(G, source, target, positions):
    """
    Perform A* search on the graph using Euclidean distance as the heuristic.
    Return the list of nodes in the path and the total cost.
    """
    def heuristic(n1, n2):
        return euclidean_distance(positions[n1], positions[n2])

    open_set = PriorityQueue()
    open_set.put((0, [source]))
    g_costs = {source: 0}

    while not open_set.empty():
        _, path = open_set.get()
        node = path[-1]

        if node == target:
            total_cost = g_costs[node]
            return (path, total_cost)

        for neighbor in G.neighbors(node):
            edge_weight = G.edges[node, neighbor]['Weight']
            new_cost = g_costs[node] + edge_weight

            if neighbor not in g_costs or new_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, target)
                new_path = path + [neighbor]
                open_set.put((priority, new_path))

    return ([], float('inf'))

def visualize_search(G, source, target, expanded_edges, final_path_edges, search_name, total_cost="N/A"):
    """
    Visualize the graph with the edges explored during a search (BFS/DFS).
    Expanded edges are colored green, while the final path is colored red.
    The source and target nodes are marked with green and red, respectively.
    """
    colors = []
    for edge in G.edges():
        if edge in final_path_edges or (edge[1], edge[0]) in final_path_edges:
            colors.append('red')  # Final path
        elif edge in expanded_edges or (edge[1], edge[0]) in expanded_edges:
            colors.append('green')  # Expanded edges
        else:
            colors.append('gray')  # Unexplored edges

    # Set node colors: green for source, red for target, and gray for others
    markers = ['green' if node == source else 'red' if node == target else 'gray' for node in G.nodes()]
    pos = nx.spring_layout(G, k=0.4, scale=2, seed=42)

    # Draw the graph with specified edge and node colors
    nx.draw(G, pos, edge_color=colors, node_color=markers, with_labels=True, node_size=800, font_size=12, font_color='black')

    # Add the final cost to the title if applicable
    plt.title(f"{search_name} Search\nFinal Cost: {total_cost}", fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{search_name.lower()}_search_result.png")
    plt.show()


def visualize_search_astar(G, source, target, search_path, search_name, total_cost):
    """
    Visualize the graph with the path found during A* search.
    Explored edges are colored orange, and the final path is red.
    The source and target nodes are marked with green and red, respectively.
    Weight of edges are included in graph (driving time).
    """
    search_edges = [(search_path[i], search_path[i + 1]) for i in range(len(search_path) - 1)] if search_path else []

    colors = []
    for edge in G.edges():
        # Check if edge exists in the path, in either direction
        if edge in search_edges or (edge[1], edge[0]) in search_edges:
            colors.append('red')  # Final path
        else:
            colors.append('gray')  # Unexplored edges

    # Color the source and target nodes differently
    markers = ['green' if node == source else 'red' if node == target else 'gray' for node in G.nodes()]

    pos = nx.spring_layout(G, k=1.0, scale=4, seed=42)

    nx.draw_networkx_nodes(G, pos, node_color=markers, node_size=800, edgecolors='black')
    nx.draw_networkx_edges(G, pos, edge_color=colors, width=2)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black', bbox=dict(facecolor="white", edgecolor='none', boxstyle='round,pad=0.2'))

    edge_labels = nx.get_edge_attributes(G, 'Weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, label_pos=0.5)

    # Add final cost as a footnote
    plt.title(f"{search_name} Search\nFinal Cost: {total_cost}", fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{search_name.lower()}.png")
    plt.show()

def main():
    """
    Main function to load the graph, prompt user for source and target nodes,
    perform BFS, DFS, and A* searches, and visualize the search results.
    """
    positions_file = 'coordinates.csv'
    edges_file = 'dataFile.csv'

    positions = load_positions_from_file(positions_file)
    graph = load_edges_from_file(edges_file)

    start_node = input("Enter the start neighborhood: ")
    target_node = input("Enter the target neighborhood: ")

    # Perform BFS search
    bfs_expanded, bfs_final_path = mybfs(graph, start_node, target_node)
    print("BFS Result", bfs_final_path)
    visualize_search(graph, start_node, target_node,bfs_expanded, bfs_final_path,'BFS',"N/A")

    # Perform DFS search
    dfs_expanded, dfs_final_path = mydfs(graph, start_node, target_node)
    print("DFS Result (edges explored):",dfs_final_path)
    visualize_search(graph, start_node, target_node,dfs_expanded, dfs_final_path,'DFS',"N/A")

    # Perform A* search
    astar_result, astar_cost = myastar(graph, start_node, target_node, positions)
    print("A* Result (path):","(",astar_result,",",astar_cost,")")
    visualize_search_astar(graph, start_node, target_node, astar_result, 'A*',astar_cost)

# Do NOT remove the following lines of code
if __name__ == "__main__":
    main()
