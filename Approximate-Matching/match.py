from functools import lru_cache


class EditDistance:
    expect = -1
    def match(self):
    
        max_iy = self.len_y
        
        # first column is from 0 to len(y)
        pre_column = range(self.len_y + 1)
        
        for i in range(self.len_x):
            # first row is always the zero
            current_column = [0]
            
            for j in range(self.len_y):
                delt = 1 if self.x[i] != self.y[j] else 0
                
                current_column.append(min(pre_column[j]+delt,pre_column[j+1]+1,current_column[j]+1))
                
            self.min_edit = min(self.min_edit,current_column[-1])

            pre_column = current_column
            if self.expect > 0:
                if self.min_edit <= self.expect:
                    break
            
            
        
    def __init__(self,x,y):
        
        # swap the x and y, the basic rule, y must be shorter than x
        if len(x) > len(y):
            self.x = x
            self.y = y
        else:
            self.y = x
            self.x = y
        
        self.len_x = len(self.x)
        self.len_y = len(self.y)
        
        self.min_edit = self.len_y

        
        
        
'''
This class simply use the edit distance with dynamic programming to solve the approximate matching problem

Some important issue:
editDistance(x,y)
length of x must be longer than y
'''
        

class EditDistanceRecursive:

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
    f.close()
    return ''.join(res)

def read_file(path):
    f = open(path,'r')
    line = f.readline().rstrip()
    res = []
    while len(line) > 0 :
        res.append(line)
        line = f.readline()
    f.close()
    return ''.join(res)
