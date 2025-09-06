from State import State
from collections import deque
import heapq
import time
# from memory_profiler import profile
# import psutil


def depth_first_search():
    closed_list = set()
    fringe = deque()

    list_max = 0
    depth_max = 0

    root = State()
    #print("Root State:"), root.display()
    fringe.append(root)

    while fringe:
        visited = fringe.popleft()

        if visited.tree_depth > depth_max:
            depth_max = visited.tree_depth

        if visited.is_goal():
            print("*" * 6)
            print("Done! State", visited.state_id, "is goal state!")
            print("Depth:", visited.tree_depth, "Max Depth:", depth_max)
            print("Path:", visited.path)
            print("Num Visited:", len(closed_list))
            print("Max Fringe Length:", list_max)
            print("Current Fringe Length:", len(fringe))
            print("*" * 6, "\n")
            break

        for direction in visited.moves:
            candidate = visited.new_state(direction, closed_list, fringe)
            if candidate is not None:
                fringe.appendleft(candidate)

        closed_list.add(visited)
        if len(fringe) > list_max:
            list_max = len(fringe)


def breadth_first_search():
    closed_list = set()
    fringe = deque()

    list_max = 0
    depth_max = 0

    root = State()
    fringe.append(root)

    while fringe:
        visited = fringe.popleft()
        if visited.tree_depth > depth_max:
            depth_max = visited.tree_depth

        if visited.is_goal():
            print("*" * 6)
            print("Done! State", visited.state_id, "is goal state!")
            print("Depth:", visited.tree_depth, "Max Depth:", depth_max)
            print("Path:", visited.path)
            print("Num Visited:", len(closed_list))
            print("Max Fringe Length:", list_max)
            print("Current Fringe Length:", len(fringe))
            print("*" * 6, "\n")
            break

        for direction in visited.moves:
            candidate = visited.new_state(direction, closed_list, fringe)
            if candidate is not None:
                fringe.append(candidate)

        closed_list.add(visited)
        if len(fringe) > list_max:
            list_max = len(fringe)


def informed_search(heuristic):
    def h1(state):
        return state.misplaced_num

    def h2(state):
        return state.distances_to_goal

    def f1(state):
        return h2(state) - h1(state)

    def score_func(state):
        pass

    closed_list = set()
    #fringe = deque()
    fringe = []

    list_max = 0
    depth_max = 0

    root = State()
    h1_min = h1(root)
    h2_min = h2(root)
    root.heuristic = heuristic
    #fringe.append(root)
    heapq.heappush(fringe, root)
    heapq.heapify(fringe)

    if heuristic == 1:
        print("Starting h1(x) Search")
    if heuristic == 2:
        print("Starting h2(x) Search")
    while fringe:
        #visited = fringe.popleft()
        visited = heapq.heappop(fringe)

        if visited.tree_depth > depth_max:
            depth_max = visited.tree_depth

        if visited.is_goal():
            print("\n" + "*" * 6)
            print("Done! State", visited.state_id, "is goal state!")
            print("Depth:", visited.tree_depth, "Max Depth:", depth_max)
            print("Path:", visited.path)
            print("Num of Moves:", len(visited.path))
            print("Num Visited:", len(closed_list))
            print("Max Fringe Length:", list_max)
            print("Current Fringe Length:", len(fringe))
            print("closed_list:", closed_list.__sizeof__(), "fringe:", fringe.__sizeof__())
            print("*"*6, "\n")
            break

        for direction in visited.moves:
            candidate = visited.new_state(direction, closed_list, fringe)

            # misplaced number of tiles
            if candidate is not None and heuristic == 1:
                if h1(visited) < h1_min:
                    h1_min = h1(visited)
                    print("Updating minimum to", h1_min, "@", time.ctime())

                heapq.heappush(fringe, candidate)
                # if h1(candidate) < h1_min or h1(candidate) < h1(visited):
                #     #fringe.appendleft(candidate)
                #     heapq.heappush(fringe, candidate)

                # if h1(candidate) < h1_min:
                #     fringe.appendleft(candidate)
                #
                # elif h1(candidate) < h1(visited):
                #     fringe.appendleft(candidate)

                # else:
                #     #fringe.append(candidate)
                #     heapq.heappush(fringe, candidate)

            # sum of distances of tiles to goal state
            elif candidate is not None and heuristic == 2:
                if h2(visited) < h2_min:
                    h2_min = h2(visited)
                    print("Updating minimum to", h2_min, "@", time.ctime())

                heapq.heappush(fringe, candidate)

                # if h2(candidate) < h2_min or h2(candidate) < h2(visited):
                #     #fringe.appendleft(candidate)
                #     heapq.heappush(fringe, candidate)

                # if h2(candidate) < h2_min:
                #     fringe.appendleft(candidate)
                #
                # elif h2(candidate) < h2(visited):
                #     fringe.appendleft(candidate)

                # else:
                #     #fringe.append(candidate)
                #     heapq.heappush(fringe, candidate)

        closed_list.add(visited)
        if len(fringe) > list_max:
            list_max = len(fringe)


# @profile(precision=8)
def main():
    while True:
        print("\n     Sliding Puzzle Solver   ")
        print("Select a search algorithm to run:")
        print("1. Breadth-First Search (BFS)")
        print("2. Depth-First Search (DFS)")
        print("3. Informed Search (Misplaced Tiles)")
        print("4. Informed Search (Manhattan Distance)")
        print("0. Quit")

        choice = input("Enter choice: ").strip()

        if choice == "0":
            print("Exiting...")
            break

        if choice == "1":
            start_time = startTime()
            breadth_first_search()
        elif choice == "2":
            start_time = startTime()
            depth_first_search()
        elif choice == "3":
            start_time = startTime()
            informed_search(1)
        elif choice == "4":
            start_time = startTime()
            informed_search(2)
        else:
            print("Invalid choice.")
            continue

        print("Ending at", time.ctime(), "\nElapsed:", (time.time() - start_time))

def startTime():
    start_time = time.time()
    print("\nStarting at", time.ctime(), "\n")
    return start_time

if __name__ == "__main__":
    main()