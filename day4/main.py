#!/usr/bin/env python3


class BingoBoard:
    def __init__(self):
        self.rows = [set() for _ in range(5)]
        self.cols = [set() for _ in range(5)]
        self.filled = 0

    def add_row(self, row):
        self.rows[self.filled] = set(row)
        for col, n in enumerate(row):
            self.cols[col].add(n)
        self.filled += 1

    def won(self):
        return not all(self.rows) or not all(self.cols)

    def play(self, n):
        for r, c in zip(self.rows, self.cols):
            r.discard(n)
            c.discard(n)
        if self.won():
            return sum(sum(row) for row in self.rows)

    def __repr__(self):
        return f"BingoBoard<rows={self.rows}, cols={self.cols}>"


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    numbers = map(int, lines[0].split(","))
    boards = []
    board = None
    for l in lines[2:]:
        if not l:
            assert board.filled == 5
            boards.append(board)
            board = None
            continue
        board = board or BingoBoard()
        board.add_row(list(map(int, l.split())))

    score = None
    winning_scores = []
    for n in numbers:
        for board in boards:
            if board.won():
                continue
            score = board.play(n)
            if score:
                winning_scores.append(score * n)
    print(winning_scores[0])
    print(winning_scores[-1])
