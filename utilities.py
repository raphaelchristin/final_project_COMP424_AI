from copy import deepcopy
import numpy as np

MOVES = ((-1, 0), (0, 1), (1, 0), (0, -1)) #moves and opposite of directions for helper functions
OPPOSITES = {0: 2, 1: 3, 2: 0, 3: 1}


def check_win(chess_board, my_pos, adv_pos):
    """check if the position has reached the ending 
    returns a tuple of a bool representing if the game is at an end state and the score
    the score is 1 if the first player wins, 0 otherwise.
    taken from the world class
    """
    board_size = chess_board.shape[0]
    father = dict()
    for r in range(board_size):
        for c in range(board_size):
            father[(r, c)] = (r, c)

    def find(pos):
        if father[pos] != pos:
            father[pos] = find(father[pos])
        return father[pos]

    def union(pos1, pos2):
        father[pos1] = pos2

    for r in range(board_size):
        for c in range(board_size):
            for dir, move in enumerate(
                MOVES[1:3]
            ):  # Only check down and right
                if chess_board[r, c, dir + 1]:
                    continue
                pos_a = find((r, c))
                pos_b = find((r + move[0], c + move[1]))
                if pos_a != pos_b:
                    union(pos_a, pos_b)

    for r in range(board_size):
        for c in range(board_size):
            find((r, c))
    p0_r = find(tuple(my_pos))
    p1_r = find(tuple(adv_pos))
    p0_score = list(father.values()).count(p0_r)
    p1_score = list(father.values()).count(p1_r)
    if p0_r == p1_r:
        return False, 0
    if p0_score == p1_score:
        return True, 0
    return True, max(0, (p0_score-p1_score)/abs(p0_score-p1_score))

def get_moves(chess_board, my_pos, adv_pos, max_step):
    """gets max_step*2 random moves from
    returns a list of random moves
    """
    moves = set()
    for i in range(max_step*4):
        moves.add(get_random_move(chess_board, my_pos, adv_pos, max_step))

    return list(moves)

def apply_move(chess_board, r, c, dir):
    """
    returns the position that results from applying the mvoe to the board, as a board (np array).
    from world class
    """
    board = deepcopy(chess_board)
    # Set the barrier to True
    board[r, c, dir] = True
    # Set the opposite barrier to True
    move = MOVES[dir]
    board[r + move[0], c + move[1], OPPOSITES[dir]] = True
    return board

def get_random_move(chess_board, my_pos, adv_pos, max_step):
    """returns a random move from the given position, as a r,c,dir tuple
    taken from the world class
    """
    # Moves (Up, Right, Down, Left)
    ori_pos = deepcopy(my_pos)
    steps = np.random.randint(0, max_step + 1)

    # Random Walk
    for _ in range(steps):
        r, c = my_pos
        dir = np.random.randint(0, 4)
        m_r, m_c = MOVES[dir]
        my_pos = (r + m_r, c + m_c)

        # Special Case enclosed by Adversary
        k = 0
        while chess_board[r, c, dir] or my_pos == adv_pos:
            k += 1
            if k > 300:
                break
            dir = np.random.randint(0, 4)
            m_r, m_c = MOVES[dir]
            my_pos = (r + m_r, c + m_c)

        if k > 300:
            my_pos = ori_pos
            break

    # Put Barrier
    dir = np.random.randint(0, 4)
    r, c = my_pos
    while chess_board[r, c, dir]:
        dir = np.random.randint(0, 4)

    return my_pos, dir    