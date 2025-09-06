import copy

# global variable, unsure how to track across project otherwise
num_states = 0


class State:
    # goal_state = [[1, 2], [3, 0]]
    # init_state = [[0, 3], [2, 1]]

    # lecture test state
    # goal_state = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    # init_state = [[2, 4, 3], [1, 7, 5], [6, 0, 8]]

    # goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    # init_state = [[1, 8, 0], [4, 3, 2], [5, 7, 6]]

    # 4x4
    # goal_state = [[1, 2, 3, 4],
    #               [5, 6, 7, 8],
    #               [9, 10, 11, 12],
    #               [13, 14, 15, 0]]
    #
    # init_state = [[10, 3, 6, 4],
    #               [1, 5, 8, 0],
    #               [2, 13, 7, 15],
    #               [14, 9, 12, 11]]

    # assignment 5x5
    init_state = [[9, 24, 3, 5, 17],
                 [6, 0, 13, 19, 10],
                 [11, 21, 22, 1, 20],
                 [16, 4, 14, 12, 15],
                 [8, 18, 23, 2, 7]]

    goal_state = [[1, 2, 3, 4, 5],
                 [6, 7, 8, 9, 10],
                 [11, 12, 13, 14, 15],
                 [16, 17, 18, 19, 20],
                 [21, 22, 23, 24, 0]]

    tree_depth = 0
    size = len(init_state)
    parent_state_id = -1
    blank_index = []

    def __init__(self, parent=None, direction=None):
        global num_states

        self.state_id = num_states
        self.moves = []
        self.path = []
        self.personal_cost = 0
        self.path_cost = 0
        self.misplaced_num = 0
        self.distances_to_goal = 0
        self.heuristic = 0

        if parent is not None:
            self.parent_state_id = parent.state_id
            self.tree_depth = parent.tree_depth + 1
            self.path = [direction for direction in parent.path]
            self.heuristic = parent.heuristic

        if direction is not None:
            self.move_blank(direction)

        self.set_blank_index()
        self.possible_moves()
        self.set_misplaced_tiles()
        self.set_distances_to_goal()

        num_states += 1

    def __del__(self):
        global num_states
        # print("Deleting...")
        num_states -= 1

    def __eq__(self, other):
        # print("__eq__:", self.init_state == other.init_state)
        s = [item for sublist in self.init_state for item in sublist]
        o = [item for sublist in other.init_state for item in sublist]
        # print("self:", s)
        # print("other:", o)
        return s == o

    def __hash__(self):
        """
            Cannot hash a list, set or dict for comparisons in set()
            set() only properly compares non-mutable objects
            Turn the nested list into a nested tuple
        """
        init_state_tup = (tuple(row) for row in self.init_state)
        # print(init_state_tup)
        # print(hash(init_state_tup))
        return hash(init_state_tup)

    def __lt__(self, other):
        """
            Required definition for heapq API
        """
        if self.heuristic == 1:
            return self.misplaced_num < other.misplaced_num
        if self.heuristic == 2:
            return self.distances_to_goal < other.distances_to_goal

    def is_goal(self):
        if self.init_state == self.goal_state:
            return True
        else:
            return False
    
    def new_state(self, direction, closed_list, fringe):
        # print("Creating new child of", self.state_id, end="-")
        new_child = State(self)
        # print("State:", new_child.state_id)
        new_child.init_state = copy.deepcopy(self.init_state)
        new_child.move_blank(direction)
        new_child.set_misplaced_tiles()
        new_child.set_distances_to_goal()
        
        """
            Maybe this should be moved to search functions, so I don't
            have to return anything or pass in closed_list, fringe
        """
        if new_child not in closed_list and new_child not in fringe:
            return new_child
        else:
            # print("State already in closed_list or fringe. Deleting...")
            # for new_child in closed_list:
            #   new_child.display()
            del new_child

    def possible_moves(self):
        self.moves.clear()

        # blank not on upper border
        if self.blank_space_index[0] > 0:
            self.moves.append('U')
        
        # blank not on lower border
        if self.blank_space_index[0] < self.size - 1:
            self.moves.append('D')
        
        # blank not on left border
        if self.blank_space_index[1] > 0:
            self.moves.append('L')

        # blank not on right border
        if self.blank_space_index[1] < self.size - 1:
            self.moves.append('R')

        # print("End possible_moves (%d):" % self.state_id, self:moves)

    def move_blank(self, direction):
        """
        1  2  3             1  2  3
        4  5  X     --->    4  5  6
        7  8  6             7  8  X
        :param direction: U, D, L, R
        :return:
        """
        x, y = self.set_blank_index()
        if direction == 'U':
            self.init_state[x][y] = self.init_state[x-1][y]
            self.init_state[x-1][y] = 0

        elif direction == 'D':
            self.init_state[x][y] = self.init_state[x+1][y]
            self.init_state[x+1][y] = 0

        elif direction == 'L':
            self.init_state[x][y] = self.init_state[x][y-1]
            self.init_state[x][y-1] = 0

        elif direction == 'R':
            self.init_state[x][y] = self.init_state[x][y+1]
            self.init_state[x][y+1] = 0

        self.set_blank_index()
        self.set_misplaced_tiles()
        self.set_distances_to_goal()
        self.path.append(direction)

    def set_misplaced_tiles(self):
        self.misplaced_num = 0
        init_tuple = tuple(j for i in self.init_state for j in i)
        goal_tuple = tuple(j for i in self.goal_state for j in i)

        # print("init:", init_tuple)
        # print("goal:", goal_tuple)
        for num in init_tuple:
            if num != 0 and init_tuple.index(num) != goal_tuple.index(num):
                # print("[{}]".format(num), init_tuple.index(num), "!=", goal_tuple.index(num))
                self.misplaced_num += 1

    def set_distances_to_goal(self):
        """
            Sum of distances for each piece to reach their goal location
        """
        # self.distances_to_goal = 0
        init_tuple = tuple(j for i in self.init_state for j in i)
        goal_tuple = tuple(j for i in self.goal_state for j in i)

        """ https://github.com/buraktekin/8-puzzle/blob/master/8-puzzle.py """
        test = 0
        for num in init_tuple:
            if num != 0:
                # print(num, ":", init_tuple.index(num), "vs", goal_tuple.index(num), end=' = ')
                # print(abs(init_tuple.index(num) - goal_tuple.index(num)))
                diff = abs(goal_tuple.index(num) - init_tuple.index(num))
                _x = diff % self.size
                _y = diff // self.size
                test += (_x + _y)

        """https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle"""
        t_sum = sum(abs((val - 1) % self.size - i % self.size) + abs((val - 1) // self.size - i // self.size)
                    for i, val in enumerate(init_tuple) if val)

        # print()
        # for row in range(self.size):
        #     print(self.init_state[row])
        # print("init:", init_tuple)
        # print("goal:", goal_tuple)
        # print("Sum:", t_sum, test)

        if t_sum <= test:
            self.distances_to_goal = t_sum
        elif test < t_sum:
            self.distances_to_goal = test

        # test_sum = 0
        # for row in range(self.size):
        #     for col in range(len(self.init_state[row])):
        #         val = self.init_state[row][col]
        #         print("{0} @ ({1},{2})".format(val, row, col), end=" vs " )
        #         x_init = row
        #         y_init = col
        #
        #         x_goal = goal_tuple.index(val)
        #         y_goal = goal_tuple.index(val)
        #         # print(x_init, y_init, end=" vs ")
        #         print("({0},{1})".format(x_goal, y_goal))
        #
        #         print("{0} moves: {1}".format(val, abs(x_init - x_goal) + abs(y_init - y_goal)))
        #         test_sum += (abs(x_init - x_goal) + abs(y_init - y_goal))

        # print("Sum:", test_sum)

    """ Removing this since my index should be tracked. """
    # def find_index(self, piece_number):
    #     for row in range(self.size):
    #         for column in range(len(self.init_state[row])):
    #             if piece_number is self.init_state[row][column]:
    #                 return row, column

    def set_blank_index(self):
        for row in range(self.size):
            for column in range(len(self.init_state[row])):
                if self.init_state[row][column] == 0:
                    self.blank_space_index = (row, column)
                    self.possible_moves()
                    return row, column

    def display(self):
        print("State:", self.state_id, "Depth:", self.tree_depth)
        print("Parent:", self.parent_state_id, "Blank:", self.blank_space_index)
        print("Path:", self.path, "Misplaced #:", self.misplaced_num)
        for row in range(self.size):
            print(self.init_state[row])
        print("Possible Moves:", self.moves)


def main():
    pass


if __name__ == "__main__":
    pass
