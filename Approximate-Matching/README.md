## What include?
This is the approximate matching program, containing the approximate matching with iterative method and recursive method. And there is a simple test code for testing the time complexity performance related to the length of the string.
## How to run?
python3 test.py
## What is include in match.py?
- read_fasta(file path) : for reading the fasta file into string
- read_fastq(file path) : for reading the fastq file into string
- EditDistance(T, P): input the string of genome sequence, T is reference Genome P is contamination genome
- Editdistance.match() run the matching
- Editdistance.min_edit: the edit distance between two genome

You can also use the recursive one, but cautious with possible memory leak!
- EditdistanceRecursive(T,P)
- EditdistanceRecursive.find()
- EditdistanceRecursive.min_edit
