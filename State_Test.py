from State import State
from collections import deque
import time


def test_init():
    root = State()
    print("root state:")
    root.display()


def test_is_goal():
    root = State()
    root.display()
    print("Goal?:", root.is_goal(), "\n")

    s1 = State(root)
    s1.init_state = s1.goal_state
    s1.set_misplaced_tiles()
    s1.set_blank_index()
    s1.display()
    print("Goal?:", s1.is_goal())


def test_move_blank():
    s1 = State()
    s1.display()

    s1.move_blank('D')
    s1.display()

    s2 = State(s1, 'R')
    s2.display()


def test_set_distances_to_goal():
    s1 = State()
    s1.display()

    s1.set_distances_to_goal()

    s2 = State()
    s2.init_state = s2.goal_state
    s2.set_distances_to_goal()

    s3 = State()
    s3.init_state = [[5, 0, 8],
                     [4, 2, 1],
                     [7, 3, 6]]
    s3.goal_state = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]
    s3.set_distances_to_goal()

    s4 = State()
    s4.init_state = [[9, 24, 3, 5, 17],
                    [6, 0, 21, 19, 10],
                    [11, 22, 13, 12, 20],
                    [16, 4, 1, 14, 15],
                    [8, 18, 23, 2, 7]]

    s4.goal_state = [[1, 2, 3, 4, 5],
                     [6, 7, 8, 9, 10],
                     [11, 12, 13, 14, 15],
                     [16, 17, 18, 19, 20],
                     [21, 22, 23, 24, 0]]
    s4.set_distances_to_goal()
    print(s4.distances_to_goal)
    s4.display()


def test_set_misplaced_tiles():
    s1 = State()
    s1.init_state = [[1, 8, 3], [4, 6, 2], [5, 7, 0]]
    s1.set_misplaced_tiles()
    s1.display()

    s2 = State()
    s2.init_state = s2.goal_state
    s2.set_misplaced_tiles()
    s2.display()

    s3 = State()
    s3.init_state = [[5, 0, 8],
                     [4, 2, 1],
                     [7, 3, 6]]
    s3.goal_state = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]
    s3.set_misplaced_tiles()
    s3.display()


def main():
    start_time = time.time()
    print("Starting at", time.ctime())

    test_set_misplaced_tiles()

    print("Ending at", time.ctime())
    print("Elapsed:", (time.time() - start_time))


if __name__ == "__main__":
    main()