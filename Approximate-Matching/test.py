import sys
from match import EditDistance, read_fastq, read_fasta
import threading
threading.stack_size(2**26)
sys.setrecursionlimit(10**6)
a = read_fasta('output.fastq')
b = read_fastq('SRR6756023.fastq')

ed = EditDistance(b,a)
threading.Thread(target = ed.find()).start()
