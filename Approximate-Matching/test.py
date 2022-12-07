
from match import EditDistance, read_fastq, read_fasta, read_file, EditDistanceRecursive



p = read_file('p1.txt')
t = read_file('t1.txt')

ed = EditDistance(p,t)
ed.expect = 1000
ed.match()

print(ed.min_edit)




