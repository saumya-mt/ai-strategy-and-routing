# Adversary

A description of one adversarial search used for this assignment. This flowchart is written in pseudocode so do not expect the statements to align with Python exactly.

## minimax

```mermaid
flowchart TD
    start(("Start"))
    start --> check["check for empty"]
    check --> id0["do a topological sort"]
    id0 --> id1["find heights of each node"]
    id1 --> id2["figure out which nodes are leaves"]
    id2 --> leaf{"len(leaves) > 1?"}
    leaf --"yes"--> parents["init parents set"]
    parents --> findParents["add parents of the leaves to parents set"]
    findParents --> getChildren{"for each parent p"}
    getChildren --> getC2["find it's children"]
    getC2 --> checkp{"p has no utility"}
    checkp --"yes"--> addbest["best ← p's first child's utility"]
    checkp --"no"--> addbest2["best ← p's utility"]
    addbest --> next["h ← heights[p]<br />player ← h % 2"]
    addbest2 --> next
    next --> checkfor{"for each child in p's children"}
    checkfor --> if{"best[player] < child's utility for the player"}
    if --"yes"--> updatebest["best ← child's utility"]
    updatebest --> remove["remove the edge from p to child"]
    if --"no" --> remove
    remove --> checkfor
    checkfor --"complete"--> newbest["p's utility ← best"]
    newbest --> getChildren
    getChildren --"complete"--> nomore{"len(parents) is 1?"}
    nomore --"yes"--> return["return player 0's best"]
    return --> stop
    nomore --"no"--> getleaves["update the leaves"]
    getleaves --> leaf
    leaf --"no"--> final["return the root's utility for player 0"]
    stop(("Stop"))
    final --> stop
    
```

Note: This is an iterative version of the algorithm. The left arrow (←) means assign to. Consider using `list(nx.topological_sort(G))`, `nx.shortest_path_length(G,sorted[0])`, and `[x for x in G.nodes() if G.out_degree(x)==0 and G.in_degree(x)==1]` as helpful snippets of code. You can access utility using commands like `G.nodes[p]["utility"]`.

## AlphaBeta Pruning

This is something that you can implement as a clever update to minimax. Keep in mind that the given version of minimax removes edges to simplify the graph, but your AlphaBeta should only remove edges when they are pruning from the tree. For a helpful step-by-step guide, visit [https://www.youtube.com/watch?v=xBXHtz4Gbdo](https://www.youtube.com/watch?v=xBXHtz4Gbdo) for an in-dept explanation on an example tree by the folks at Berkeley.
