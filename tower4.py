class Tile:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = None
        self.guesses = [num + 1 for num in range(NUM_TILES)]

    def set_value(self, val):
        if self.value is not None and self.value != val:
            print("WARN: Trying to set existing value from " + str(self.value) + " to " + str(val))
        self.value = val
        self.guesses = []

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


# clues are clockwise: 0..3 4..7 8..11 12..15
def solve_puzzle(the_clues):
    global clues
    clues = the_clues
    solution = [[] for num in range(NUM_TILES)]  # list of columns

    # for i in range(16):
    #    board[i].set_value(i)
    # for i in range(16):
    #    print(get_line(i))
    # print_board()
    fill_trivial_cases()
    print_board()
    fill_last_element()
    fill_last_occurence()
    print_board()
    # try to find numbers that are 3 times in the board and write in the 4th
    # eliminate possibilities based on LUTs

    solution = [[] for num in range(NUM_TILES)]
    for i in range(NUM_TILES):
        for k in range(NUM_TILES):
            solution[k].append(board[k * NUM_TILES + i])
    for i in range(NUM_TILES):
        solution[i] = tuple(solution[i])
    solution = tuple(solution)
    return solution


def get_line(index):  # TODO make this generic
    ret = []
    for k in range(NUM_TILES):
        if index < 4:
            ret.append(board[index + k * 4])
        elif index < 8:
            ret.append(board[(index - 3) * 4 - k - 1])
        elif index < 12:
            ret.append(board[23 - index - k * 4])
        else:
            ret.append(board[(15 - index) * 4 + k])
    return ret


# fills a line if one element is missing
def fill_last_element():
    for i in range(NUM_TILES * 2):
        line = get_line(i)
        found = [False for num in range(NUM_TILES)]
        for tile in line:
            if tile.value is not None:
                found[tile.value - 1] = True
        if found.count(False) == 1:
            to_fill = found.index(False)
            for tile in line:
                if tile.value is None:
                    tile.value = to_fill + 1
                    break


def fill_last_occurence():
    for i in range(1, NUM_TILES + 1):
        h_missing = [num for num in range(NUM_TILES)]
        v_missing = [num for num in range(NUM_TILES)]
        for a_tile in board:
            if a_tile.value == i:
                h_missing.remove(a_tile.x)
                v_missing.remove(a_tile.y)
        if len(h_missing) == 1:
            board[h_missing[0] + v_missing[0] * NUM_TILES].set_value(i)


# fills if clues are 1 or NUM_TILES
def fill_trivial_cases():
    for i in range(len(clues)):
        line = get_line(i)
        if clues[i] == 1:  # line begins with NUM_TILES
            line[0].set_value(NUM_TILES)
        elif clues[i] == NUM_TILES:  # line is 1,2,3,..
            for k in range(NUM_TILES):
                line[k].set_value(k + 1)


def print_board():
    for i in range(NUM_TILES):
        for j in range(NUM_TILES):
            print(" " + str(board[i * NUM_TILES + j]), end='')
        print()
    print()

NUM_TILES = 4
board = [Tile(num % NUM_TILES, num // NUM_TILES) for num in range(NUM_TILES * NUM_TILES)]
# board[0].set_value(3)
# board[7].set_value(3)
# board[10].set_value(3)
clues = None
# solve_puzzle((0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0))
solve_puzzle((2,2,1,3, 2,2,3,1, 1,2,2,3, 3,2,1,3))