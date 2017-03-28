class Tile:

    def __init__(self):
        self.value = None
        self.guesses = [1, 2, 3, 4]

    def set_value(self, val):
        if self.value is not None and self.value != val:
            print("WARN: Trying to set existing value from " + str(self.value) + " to " + str(val))
        self.value = val
        self.guesses = []

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

board = [Tile() for num in range(16)]
clues = None


# clues are clockwise: 0..3 4..7 8..11 12..15
def solve_puzzle(the_clues):
    global clues
    clues = the_clues
    solution = [[] for num in range(4)]  # list of columns

    # for i in range(16):
    #    board[i].set_value(i)
    # for i in range(16):
    #    print(get_line(i))
    # print_board()
    fill_trivial_cases()
    print_board()

    # repeat:

    # try to find lines with 3 filled elements and fill the 4th
    board[5].set_value(3)
    board[6].set_value(2)
    board[7].set_value(4)
    fill_4th_element()
    print_board()
    # try to find numbers that are 3 times in the board and write in the 4th
    # eliminate possibilities based on LUTs

    solution = [[], [], [], []]
    for i in range(4):
        for k in range(4):
            solution[k].append(board[i * 4 + k])
    for i in range(4):
        solution[i] = tuple(solution[i])
    solution = tuple(solution)
    return solution


def get_line(index):
    ret = []
    for k in range(4):
        if index < 4:
            ret.append(board[index + k * 4])
        elif index < 8:
            ret.append(board[(index - 3) * 4 - k - 1])
        elif index < 12:
            ret.append(board[23 - index - k * 4])
        else:
            ret.append(board[(15 - index) * 4 + k])
    return ret


def fill_4th_element():
    for i in range(8):
        line = get_line(i)
        found = [False, False, False, False]
        for tile in line:
            if tile.value is not None:
                found[tile.value - 1] = True
        if found.count(False) == 1:
            to_fill = found.index(False)
            for tile in line:
                if tile.value is None:
                    tile.value = to_fill + 1
                    break


# fills if clues are 1 or 4
def fill_trivial_cases():
    for i in range(len(clues)):
        line = get_line(i)
        if clues[i] == 1:  # line begins with 4
            line[0].set_value(4)
        elif clues[i] == 4:  # line is 1,2,3,4
            for k in range(4):
                line[k].set_value(k + 1)


def print_board():
    for i in range(4):
        for j in range(4):
            print(str(board[i * 4 + j].value) + " ", end='')
        print()
    print()

solve_puzzle([0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0])