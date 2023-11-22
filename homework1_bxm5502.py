############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "Benjamin Mashkevich"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from math import factorial

import random

import copy

from collections import deque
############################################################
# Section 1: N-Queens
############################################################


def comb(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))


def num_placements_all(n):
    return comb((n * n), n)


def num_placements_one_per_row(n):
    return n ** n


def n_queens_valid(board):
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] == board[j]:
                return False
            if abs(board[i] - board[j]) == abs(i - j):
                return False
    return True


def n_queens_helper(n, board):
    if len(board) == n:
        yield board[:]
        return
    for c in range(n):
        board.append(c)
        if n_queens_valid(board):
            yield from n_queens_helper(n, board)
        board.pop()


def n_queens_solutions(n):
    yield from n_queens_helper(n, [])


############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < len(self.board) and 0 <= nc < len(self.board[0]):
                self.board[nr][nc] = not self.board[nr][nc]

    def scramble(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col]:
                    return False
        return True

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                n_board = self.copy()
                n_board.perform_move(row, col)
                yield (row, col), n_board

    def find_solution(self):
        frontier = deque()
        frontier.append(([], self))
        visited = set()
        while frontier:
            c_path, status = frontier.popleft()
            if status.is_solved():
                return c_path
            c_board = tuple(tuple(row) for row in status.get_board())
            if c_board in visited:
                continue
            visited.add(c_board)
            for move, n_status in status.successors():
                n_path = list(c_path)
                n_path.append(move)
                frontier.append((n_path, n_status))
        return None


def create_puzzle(rows, cols):
    board = [[False] * cols for _ in range(rows)]
    return LightsOutPuzzle(board)


############################################################
# Section 3: Linear Disk Movement
############################################################


def find_identical(puzzle, length):
    def swap_yield(src, tar):
        puzzle[src], puzzle[tar] = puzzle[tar], puzzle[src]
        yield (src, tar), list(puzzle)
        puzzle[src], puzzle[tar] = puzzle[tar], puzzle[src]
    for i in range(length - 1):
        if not puzzle[i]:
            continue
        if i + 2 < length and puzzle[i + 1] and not puzzle[i + 2]:
            yield from swap_yield(i, i + 2)
        if not puzzle[i + 1]:
            yield from swap_yield(i, i + 1)


def solve_identical_disks(length, n):
    def id_state():
        src = [True if x < n else False for x in range(length)]
        dest = [False if x < length - n else True for x in range(length)]
        return src, dest
    src, dest = id_state()
    if length == 0 or src == dest:
        return []
    visited = set()
    frontier = deque([([], src)])
    while frontier:
        path, curr = frontier.popleft()
        for move, n_state in find_identical(curr, length):
            new = path + [move]
            if n_state == dest:
                return new
            state = tuple(n_state)
            if state not in visited:
                visited.add(state)
                frontier.append((new, n_state))
    return 0


def find_distinct(puzzle, length):
    for i in range(length):
        if puzzle[i] == 0:
            continue
        tmp = puzzle.copy()
        poss = [
            (i, i + 2, lambda x: x + 1 < length and puzzle[x + 1] and x + 2 < length and puzzle[x + 2] == 0),
            (i, i + 1, lambda x: x + 1 < length and puzzle[x + 1] == 0),
            (i, i - 2, lambda x: x - 1 >= 0 and puzzle[x - 1] and x - 2 >= 0 and puzzle[x - 2] == 0),
            (i, i - 1, lambda x: x - 1 >= 0 and puzzle[x - 1] == 0)
        ]
        for src, dst, condition in poss:
            if condition(src):
                puzzle[src], puzzle[dst] = puzzle[dst], puzzle[src]
                yield ((src, dst), puzzle)
                puzzle = tmp.copy()


def solve_distinct_disks(length, n):
    src = [i + 1 if i < n else False for i in range(length)]
    dest = [False if i < length - n else length - i for i in range(length)]
    if length == 0 or src == dest:
        return []
    visited = set()
    frontier = deque([([], src)])
    while frontier:
        path, current = frontier.popleft()
        for move, new in find_distinct(current, length):
            if new == dest:
                return path + [move]
            new_entry = (path + [move], new)
            state = tuple(new)
            if state not in visited:
                frontier.append(new_entry)
                visited.add(state)
    return 0


############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
Approximately 20 hours 
"""

feedback_question_2 = """
In the N-Queens portion of this assignment, I found myself stuck
trying to test print(list(n_queens_solutions(15))) and thought
I needed to optimize my code further, but incorporating a loop
that prints print(next(solutions)) 15 times where solutions
iterates through n_queens_solutions(15) gave me a correct and
efficient output.
"""

feedback_question_3 = """
I liked the test cases that were included in the instructions page
however I would like it if there were more clear test cases
that tell me if my code works so I don't have to put myself through
the lengthy process of trying to optimize my n-queens code when
it wasn't needed. That may just be me but I feel like explicit testing
instructions are significantly beneficial to my personal efficiency
when dealing with a homework assignment that has a target output.
"""
