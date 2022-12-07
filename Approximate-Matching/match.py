from functools import lru_cache
'''
This class simply use the edit distance with dynamic programming to solve the approximate matching problem

Some important issue:
editDistance(x,y)
length of x must be longer than y
'''


class editDistance:
    min_edit = 0

    @lru_cache(None)
    def match(self,ix, iy):
        if iy == -1:
            return 0

        if ix == -1:
            return iy + 1

        return min(self.match(ix, iy-1) + 1, self.match(ix-1, iy) + 1, self.match(ix-1, iy-1) + (1 if self.x[ix] != self.y[iy] else 0))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        max_iy = len(y) - 1
        self.min_edit = len(y)

        for ix in range(len(x)):
            self.min_edit = min(self.min_edit, self.match(ix, max_iy))

            if self.min_edit == 0:
                break
