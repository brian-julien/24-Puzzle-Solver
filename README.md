# 24-Puzzle Solver
A project that implements search algorithms to solve a sliding puzzle of 24 pieces (5 x 5 tiles).
This project demonstrates fundamental knowledge of artificial intelligence, heuristics, and algorithm optimization by comparing uninformed and informed search strategies.

## Features
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Informed Search with two heuristics:
    - Misplaced Tiles: number of tiles not in their goal position
    - Manhattan Distance: sum of distances from each tile to its goal position

## Highlights
- Custom State class to represent puzzle boards, track moves, and calculate heuristic values  
- Efficient state hashing and equality checks to avoid revisiting explored states  
- Use of priority queues (`heapq`) for informed search optimization

## Installation and Usage
Requires **Python 3.x**.

Clone the repo:
```
git clone https://github.com/brian-julien/24-Puzzle-Solver
cd 24-Puzzle-Solver
```
Run the solver with:
```
python Searches.py
```

## Example Output
When a solution is found, the program reports:
- Solution pathing (sequence of moves)  
- Number of moves  
- States visited  
- Maximum depth reached  
- Fringe statistics  
