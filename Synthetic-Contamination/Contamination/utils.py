

def read_fastq(filename):

    cur_read = []
    with open(filename, "r", encoding="utf-8") as fr:
        for line in fr:
            cur_read.append(line)

            if len(cur_read) == 4:
                yield "".join(cur_read)
                cur_read = []


def read_fasta_individual(filename):

    cur_read = []
    with open(filename, "r", encoding="utf-8") as fr:
        lines = fr.readlines()
        return lines[1::2]

def read_fasta(filename):

    cur_read = []
    seq_line_bool = False
    with open(filename, "r", encoding="utf-8") as fr:
        for line in fr:
            cur_read.append(line)

            if len(cur_read) == 2:
                yield "".join(cur_read)
                cur_read = []


