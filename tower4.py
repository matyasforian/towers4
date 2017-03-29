class Tile:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = None
        self.guesses = {1, 2, 3, 4}

    def set_value(self, val):
        if self.value is not None and self.value != val:
            print("WARN: Trying to set existing value from " + str(self.value) + " to " + str(val))
        self.value = val
        self.guesses = set()

    def __str__(self):
        if self.value is None:
            return "."
        return str(self.value)

    def __repr__(self):
        return self.__str__()


# clues are clockwise: 0..3 4..7 8..11 12..15
def solve_puzzle(clues):
    print(clues)
    board = [Tile(num % NUM_TILES, num // NUM_TILES) for num in range(NUM_TILES * NUM_TILES)]
    solution = [[] for num in range(NUM_TILES)]  # list of columns

    fill_trivial_cases(board, clues)

    for i in range(10):
        print_board(board)
        fill_last_element(board)
        fill_last_occurence(board)
        eliminate_LUT(board, clues)
        eliminate_guess(board)
        fill_single_guess(board)
        if is_done(board):
            break

    print_board(board)

    solution = [[] for num in range(NUM_TILES)]
    for i in range(NUM_TILES):
        for k in range(NUM_TILES):
            solution[k].append(board[k * NUM_TILES + i].value)
    for i in range(NUM_TILES):
        solution[i] = tuple(solution[i])
    solution_tup = tuple(solution)
    return solution_tup


def fill_single_guess(board):
    for i in range(NUM_TILES * 2):
        occurences = [0 for num in range(NUM_TILES)]
        line = get_line(board, i)
        for tile in line:
            if tile.value is not None:
                occurences[tile.value - 1] = 999
            else:
                for guess in tile.guesses:
                    occurences[guess - 1] = occurences[guess - 1] + 1
        for k in range(len(occurences)):
            if occurences[k] == 1:
                for tile in line:
                    if k + 1 in tile.guesses:
                        tile.set_value(k + 1)
                        # this is not optimized. it should update the guesses and continue to check stuff
                        return


def eliminate_guess(board):
    for i in range(NUM_TILES * 2):
        line = get_line(board, i)
        to_elim = []
        for tile in line:
            if tile.value is not None:
                to_elim.append(tile.value)
        for tile in line:
            if tile.value is None:
                for elim in to_elim:
                    tile.guesses.discard(elim)
                if len(tile.guesses) == 1:
                    tile.set_value(tile.guesses.pop())
                    break


def is_done(board):
    left = NUM_TILES * NUM_TILES
    for tile in board:
        if tile.value is not None:
            left = left - 1
    return left == 0


def get_line(board, index):  # TODO make this generic
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


def eliminate_LUT(board, clues):
    for i in range(NUM_TILES * 4):
        if clues[i] == 2:
            line = get_line(board, i)
            match_line(LUT2, line)
        if clues[i] == 3:
            line = get_line(board, i)
            match_line(LUT3, line)


def match_line(lut, line):
    all_sols = []
    for possible_sol in lut:
        good_sol = True
        for i in range(NUM_TILES):
            if line[i].value is not None and line[i].value != possible_sol[i]:
                good_sol = False
                break
        if good_sol:
            all_sols.append(possible_sol)

    ret = []
    for k in range(NUM_TILES):
        sols = set()
        for sol in all_sols:
            sols.add(sol[k])
        ret.append(sols)
    for m in range(NUM_TILES):
        line[m].guesses.intersection_update(ret[m])
        if len(line[m].guesses) == 1:
            line[m].set_value(line[m].guesses.pop())


# fills a line if one element is missing
def fill_last_element(board):
    for i in range(NUM_TILES * 2):
        line = get_line(board, i)
        found = [False for num in range(NUM_TILES)]
        for tile in line:
            if tile.value is not None:
                found[tile.value - 1] = True
        if found.count(False) == 1:
            to_fill = found.index(False)
            for tile in line:
                if tile.value is None:
                    tile.set_value(to_fill + 1)
                    break


def fill_last_occurence(board):
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
def fill_trivial_cases(board, clues):
    for i in range(len(clues)):
        line = get_line(board, i)
        if clues[i] == 1:  # line begins with NUM_TILES
            line[0].set_value(NUM_TILES)
        elif clues[i] == NUM_TILES:  # line is 1,2,3,..
            for k in range(NUM_TILES):
                line[k].set_value(k + 1)


def print_board(board):
    for i in range(NUM_TILES):
        st = ""
        for j in range(NUM_TILES):
            st = st + " " + str(board[i * NUM_TILES + j])
        print(st)
    print("  ")

LUT2 = ((1, 4, 2, 3),
        (1, 4, 3, 2),
        (2, 1, 4, 3),
        (2, 4, 1, 3),
        (2, 4, 3, 1),
        (3, 4, 1, 2),
        (3, 4, 2, 1),
        (3, 1, 4, 2),
        (3, 2, 4, 1),
        (3, 1, 2, 4),
        (3, 2, 1, 4))

LUT3 = ((1, 2, 4, 3),
        (1, 3, 4, 2),
        (1, 3, 2, 4),
        (2, 1, 3, 4),
        (2, 3, 1, 4),
        (2, 3, 4, 1))

NUM_TILES = 4

# solve_puzzle((2, 2, 1, 3,  2, 2, 3, 1,  1, 2, 2, 3,  3, 2, 1, 3))
solve_puzzle((0, 2, 0, 0,  0, 3, 0, 0,  0, 1, 0, 0,  0, 0, 1, 2))
