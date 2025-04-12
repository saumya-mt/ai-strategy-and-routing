# AI Projects: Advanced Problem Solving with Intelligent Algorithms

This repository showcases my approach to solving complex computational problems using systematic problem-solving methodologies and advanced algorithms.

## Project 1: Building a Competitive Chess AI

### Problem Analysis
Chess presents several computational challenges:
- Exponential growth of possible moves (branching factor ~35)
- Need for real-time decision making
- Complex position evaluation
- Balancing between search depth and performance

### Solution Methodology
1. **Problem Decomposition**:
   - Broke down chess into core components: move generation, position evaluation, and search
   - Identified critical performance bottlenecks

2. **Algorithm Selection & Optimization**:
   - Implemented alpha-beta pruning to reduce search space from O(b^d) to O(b^(d/2))
   - Used iterative deepening for time management
   - Applied machine learning (Lasso regression) for position evaluation

3. **Performance Optimization**:
   - Reduced move generation overhead
   - Optimized position evaluation using bitboards
   - Implemented efficient data structures for move ordering

4. **Validation & Testing**:
   - Created tournament system for AI vs AI matches
   - Used FEN notation for position analysis and debugging
   - Compared performance against different search depths

### Key Insights
- Demonstrated how to balance between search depth and evaluation quality
- Showed the importance of move ordering in alpha-beta pruning
- Proved the effectiveness of machine learning in position evaluation

## Project 2: Optimizing Pathfinding in Real-World Maps

### Problem Analysis
Real-world pathfinding presents unique challenges:
- Large search spaces with complex constraints
- Need for different optimization criteria (distance, time, cost)
- Real-world geographical constraints
- Requirement for both optimal and heuristic solutions

### Solution Methodology
1. **Problem Modeling**:
   - Represented Seattle area as a weighted graph
   - Defined clear optimization criteria for different scenarios
   - Incorporated real-world geographical data

2. **Algorithm Implementation & Comparison**:
   - A* Search: Combined heuristic estimates with actual costs
   - Breadth-First Search: Guaranteed shortest path in unweighted graphs
   - Depth-First Search: Explored alternative path-finding strategies
   - Uniform Cost Search: Optimized for minimum total cost
   - Greedy Search: Quick solutions with heuristic guidance

3. **Performance Analysis**:
   - Compared time and space complexity of different algorithms
   - Analyzed trade-offs between optimality and speed
   - Evaluated heuristic effectiveness

4. **Visualization & Validation**:
   - Created visual representations of search paths
   - Validated results against real-world routes
   - Demonstrated algorithm behavior in different scenarios

### Key Insights
- Showed how different algorithms perform in real-world scenarios
- Demonstrated the importance of heuristic selection in A* search
- Proved the trade-offs between optimality and computational efficiency

## Problem-Solving Skills Demonstrated
1. **Analytical Thinking**:
   - Breaking down complex problems into manageable components
   - Identifying critical performance bottlenecks
   - Understanding trade-offs between different solutions

2. **Algorithm Design**:
   - Selecting appropriate algorithms for specific problems
   - Optimizing algorithms for real-world constraints
   - Implementing efficient data structures

3. **Validation & Testing**:
   - Creating comprehensive testing frameworks
   - Using visualization for result validation
   - Comparing different approaches systematically

4. **Performance Optimization**:
   - Reducing computational complexity
   - Balancing between different optimization criteria
   - Implementing efficient solutions

## Technical Implementation
Both projects are implemented in Python, showcasing:
- Clean, modular code architecture
- Efficient algorithm implementation
- Comprehensive documentation
- Practical testing frameworks

## Author
Saumya Mishra

## License
This project is licensed under the MIT License - see the LICENSE file for details

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Required Python packages (install using `pip install -r requirements.txt`):
  - numpy
  - pandas
  - scikit-learn
  - matplotlib
  - python-chess (for chess project)
  - networkx (for graph search project)

### Project 1: Chess AI
1. **Setup**:
   ```bash
   cd chess2-saumya-mt-main
   ```

2. **Running the Chess AI**:
   - Basic version:
     ```bash
     python killbill.py
     ```
   - Advanced version with machine learning:
     ```bash
     python killbillV2.py
     ```
   - To run tournaments:
     ```bash
     python tournament.py
     ```

3. **Features**:
   - The AI supports standard chess moves
   - Use FEN notation for position analysis
   - Tournament system for AI vs AI matches

### Project 2: Graph Search Algorithms
1. **Setup**:
   ```bash
   cd graphsearch-saumya-mt-main
   ```

2. **Running Pathfinding Algorithms**:
   ```bash
   python search.py
   ```
   This will run all implemented algorithms (A*, BFS, DFS, Uniform Cost, Greedy) on the Seattle map.

3. **Visualizing Results**:
   - The program generates PNG files showing the search paths
   - Compare different algorithms using the generated images
   - Results are saved in the project directory

4. **Customizing Search**:
   - Modify `coordinates.csv` to add new locations
   - Adjust parameters in `search.py` for different search behaviors
   - Use different heuristics by modifying the heuristic functions

### Example Usage

#### Chess AI:
```python
from killbillV2 import ChessAI

# Initialize the AI
ai = ChessAI()

# Get AI's move for a given position
move = ai.get_best_move(fen_position)
```

#### Graph Search:
```python
from search import GraphSearch

# Initialize with Seattle map data
searcher = GraphSearch('dataFile.csv')

# Find path using A* algorithm
path = searcher.a_star_search(start, goal)

# Visualize the path
searcher.visualize_path(path, 'path_visualization.png')
```

### Troubleshooting
1. **Chess AI**:
   - Ensure all dependencies are installed
   - Check if the model file (`best_model_killbillV2_Lasso.pkl`) is present
   - Verify FEN notation format when analyzing positions

2. **Graph Search**:
   - Verify CSV files are properly formatted
   - Check if coordinates are within the map boundaries
   - Ensure matplotlib is properly installed for visualization

### Additional Resources
- Chess project documentation in `algorithm.md`
- Graph search algorithms explained in `algorithms.md`
- Example visualizations in the project directories 
