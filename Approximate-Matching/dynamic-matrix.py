from functools import lru_cache
import numpy as np

@lru_cache(None)
def edDistRecursive(x,y):
    global n
    if len(x) == 0:
        return len(y)
    if len(y) == 0:
        return len(x)
        
    delt = 1 if x[-1] != y[-1] else 0
    
    return min(edDistRecursive(x[:-1],y) + 1, edDistRecursive(x,y[:-1]) + 1, edDistRecursive(x[:-1],y[:-1]) + delt)

if __name__ == '__main__':
    f1 = open('../lib/output.fastq')
    f2 = open('../lib/SRR6756023.fastq')
    f1.readline()
    f2.readline()
    
    scores = []
    
    line_f1 = f1.readline().rstrip()
    line_f2 = f2.readline().rstrip()
    
    len_str = len(line_f1)
    while len_str > 0:
        scores.append(1 - edDistRecursive(line_f1,line_f2)/len_str)
        f1.readline()
        f1.readline()
        f1.readline()
        f2.readline()
        f2.readline()
        f2.readline()
        
        line_f1 = f1.readline().rstrip()
        line_f2 = f2.readline().rstrip()
        
        len_str = len(line_f1)
    f1.close()
    f2.close()
    print(np.mean(scores))
