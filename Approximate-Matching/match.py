from functools import lru_cache
'''
This class simply use the edit distance with dynamic programming to solve the approximate matching problem

Some important issue:
editDistance(x,y)
length of x must be longer than y
'''


class EditDistance:

    @lru_cache(None)
    def match(self,ix, iy):
        if iy == -1:
            return 0

        if ix == -1:
            return iy + 1

        return min(self.match(ix, iy-1) + 1, self.match(ix-1, iy) + 1, self.match(ix-1, iy-1) + (1 if self.x[ix] != self.y[iy] else 0))

    def find(self):
        for ix in range(len(self.x)):
            self.min_edit = min(self.min_edit, self.match(ix, self.max_iy))
            if self.min_edit == 0:
                break

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.max_iy = len(y) - 1
        self.min_edit = len(y)


        print(self.min_edit)

def read_fastq(path):
    f = open(path, 'r')
    line = f.readline().rstrip()
    res = []
    while len(line) > 0:
        res.append(f.readline().rstrip())
        f.readline()
        f.readline()
        line = f.readline()

    return ''.join(res)


def read_fasta(path):
    f = open(path, 'r')
    line = f.readline().rstrip()
    res = []
    while len(line) > 0:
        res.append(f.readline().rstrip())
        line = f.readline()

    return ''.join(res)