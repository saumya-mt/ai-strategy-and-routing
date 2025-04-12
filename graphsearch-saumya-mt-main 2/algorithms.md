# Search Algorithms

A description of the search techniques used for this assignment. This flowchart is written in pseudocode so do not expect the statements to align with Python exactly.

## BFS

```mermaid
flowchart TD
    start(("Start"))
    start --> id0["init edges"]
    id0 --> id1{"empty G?"}
    id1 --"yes"--> return["return edges"]
    return --> stop(("Stop"))
    id1 --"no"-->id3["fronteir.add(source)<br />reached.add(source)"]
    id3 --> id4{"frontier empty?"}
    id4 --"yes"-->return
    id4 --"no"-->id6["c ← frontier.dequeue"]
    id6 --> id7{"c.next_child"}
    id7 --"none"--> id4
    id7 --"next"--> id8{"child ∉ reached"}
    id8 --"no"--> id7
    id8 --"yes"--> id9["edge.add(c→child)<br/>reached.add(child)<br/>frontier.add(child)"]
    id9 --> id10{"child is goal"}
    id10 --"yes"-->return
    id10 --"no"-->id7
```

Note: The left arrow (←) means assign to. The right arrow (→) means edge or the tuple connecting the parent to a child. The `child.next` statment means create a way to iterate through all of the children of a node like `for child in G.adj[current]` or using the `children` function from networkx.

---

## DFS

```mermaid
flowchart TD
    start(("Start"))
    start --> id0["init edges"]
    id0 --> id1{"empty G?"}
    id1 --"yes"--> return["return edges"]
    return --> stop(("Stop"))
    id1 --"no"-->id3["goalFound←False<br />visited.add(source)<br />currentEdge←expand(source→children)"]
    id3 --> found{"!goalFound &<br />!empty(currentEdge)"}
    found --"no"-->return
    found --"yes"-->id4["(parent,current)←popleft(currentEdge)<br />edges.add(parrent→current)<br />visited.add(current)"]
    id4 --> id5{"goal is current"}
    id5 --"yes"--> id6["goalFound←True"]
    id6 --> found
    id5 --"no"--> id7["exp←expand(current→children)<br />currentEdge.pushLeft(exp)"]
    id7 --> found
```

Note: This version pops from the left and pushes on the left, which is reversed from the normal stack. The expand function is meant to give a list of edges from the node to its children. This is because expanding is usually done in order, instead of in reverse, so you can use a normal stack (or recursion) if you reverse the node order, so the results will be in-order.

---

## A*

```mermaid
flowchart TD
    start(("Start"))
    start --> id0["init bestPath<br />bestCost←0"]
    id0 --> id1{"empty G?"}
    id1 --"yes"--> return["return (bestPath,bestCost)"]
    return --> stop(("Stop"))
    id1 --"no"-->id3["bestCost←&infin; <br />paths←PriorityQ<br />paths.put((source, [source]))"]
    id3 --> while{"!empty(paths)"}
    while --"yes"-->id4["(cost,path)←paths.get()<br/>current←end(path)<br/>trueCost←path_weight(path)"]
    id4 --> check{"trueCost > bestCost"}
    check --"yes"-->return
    check --"no"-->itr{"current.nextChild"}
    itr --"none"-->while
    itr --"next"-->notin{"child ∉ path"}
    notin --"no"-->itr
    notin --"yes"-->id5["f←trueCost+h(child)+weight(current→child)<br />newPath←copy(path).add(child)<br />paths.put((f,newPath))"]
    id5 --> checkchild{"child is goal"}
    checkchild --"no"-->itr
    checkchild --"yes"-->cost["cost←path_weight(newPath)"]
    cost --> checkcost{"cost < bestCost"}
    checkcost --"no"-->itr
    checkcost --"yes"--> id6["bestCost←cost<br />bestPath←newPath"]
    id6 --> itr
```

Notes: In Python, the way to calculate the cost of a path is use the built in `path_weight` function like `nx.path_weight(G, mypath, weight="weight")`. To access the weight between two nodes use `G.edges[u, v]['weight']` where `u` and `v` are two different nodes. For a Priority Queue, feel free to use an already built version via this import statment `from queue import PriorityQueue` at the beginning of your program.
