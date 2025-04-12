import matplotlib.pyplot as plt
import networkx as nx
import random


def createRandomGame(rounds, actions, seed=0, isZeroSum=True):
    """
    Creates random 2-player games dependent on number of number of rounds and actions
    @param rounds - number of rounds
    @param actions - number of actions per round
    @param seed - [optional][default = 0] for controlled randomness
    @param isZeroSum - [optional][default = True] when False create general sum
    @return random game
    """
    G = nx.balanced_tree(actions, rounds*2, nx.DiGraph)
    random.seed(seed)
    attrs = {}
    for node in G.nodes():
        print(node)
        if len(list(G.neighbors(node))) == 0:
            if isZeroSum:
                payoff = random.randint(-42, 42)
                attrs[node] = {"utility": (payoff, -payoff)}
            else:
                attrs[node] = {"utility": (
                    random.randint(0, 42), random.randint(0, 42))}
        else:
            attrs[node] = {"utility": None}
    nx.set_node_attributes(G, attrs)
    return G


def exampleGameTree():
    """
    Create example game from Russell & Norvig
    """
    G = nx.balanced_tree(3, 2, nx.DiGraph)
    attrs = {i: {"utility": None} for i in range(0, 13)}
    nx.set_node_attributes(G, attrs)
    H = nx.relabel_nodes(G, {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'b1', 5: 'b2',
                         6: 'b3', 7: 'c1', 8: 'c2', 9: 'c3', 10: 'd1', 11: 'd2', 12: 'd3'})
    H.nodes['b1']['utility'] = (3, -3)
    H.nodes['b2']['utility'] = (12, -12)
    H.nodes['b3']['utility'] = (8, -8)
    H.nodes['c1']['utility'] = (2, -2)
    H.nodes['c2']['utility'] = (4, -4)
    H.nodes['c3']['utility'] = (6, -6)
    H.nodes['d1']['utility'] = (14, -14)
    H.nodes['d2']['utility'] = (5, -5)
    H.nodes['d3']['utility'] = (2, -2)
    return H

def genericGameTree(p = [2,3,4,5,1,2,6,10,8,1,9,3]):
    """
    Create a game tree for the Berkeley examples
    """
    G = nx.full_rary_tree(2,15,nx.DiGraph)
    H = nx.full_rary_tree(2,7,nx.DiGraph)
    mapping = {x:x+16 for x in range(7)}
    H = nx.relabel_nodes(H, mapping)
    G.add_nodes_from(H.nodes())
    G.add_edge(0,16)
    G.add_edges_from(H.edges())
    n = list(nx.dfs_preorder_nodes(G, source=0))
    mapping = {n[i]:i for i in range(len(n))}
    G = nx.relabel_nodes(G, mapping)
    attrs = {i: {"utility": None} for i in range(len(n))}
    nx.set_node_attributes(G, attrs)
    indexes = [3,4,6,7,10,11,13,14,17,18,20,21]
    for i in range(len(indexes)):
        G.nodes[indexes[i]]['utility'] = (p[i], -p[i])
    return G