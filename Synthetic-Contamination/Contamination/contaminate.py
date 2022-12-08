
import argparse
import random
from tqdm import tqdm
import numpy as np

from utils import read_fasta, read_fasta_individual

parser = argparse.ArgumentParser()

parser.add_argument('--human_file', type=str, default="raw_data/SRR6756025_200_reads.fasta", help='Human fastq file')
parser.add_argument('--contaminate_file', type=str, default="raw_data/staphylococcus.fasta", help='Foreign DNA fastq file to contaminate human file')
parser.add_argument('--output_file', type=str, default="synthetic_data/output.fastq", help='Output file')
parser.add_argument('--contamination_length', type=int, default=50, help='The edit window length that edits will span')
parser.add_argument('--sequence_identity', type=float, default=0.50, help='The fraction of each edit window that will be editted')
parser.add_argument('--contamination_rate', type=float, default=0.01, help='The fraction of the overall template that was contaminated')
parser.add_argument('--read_based', type=int, default=0, help='Replace human reads with contaminate reads vs individual bp contamination. Only uses contamination_rate if read based.')


args = parser.parse_args()

def read_based_contaminate():
    with open(args.human_file, "r", encoding="utf-8") as fr:
        human_reads = fr.readlines()
    with open(args.contaminate_file, "r", encoding="utf-8") as fr:
        contamination_reads = fr.readlines()

    number_contaminated_reads = int((len(human_reads)/2) * args.contamination_rate)
    human_indices = random.sample(range((len(human_reads)-1)//2), k=number_contaminated_reads)
    bacterial_indices = random.sample(range((len(contamination_reads)-1)//2), k=number_contaminated_reads)
    for i in range(number_contaminated_reads):
        # Set the randomly chosen human read to the randomly chosen bacterial read
        human_reads[2 * human_indices[i] + 1] = contamination_reads[2 * bacterial_indices[i] + 1]
        # Set human read title to have the correct line length
        human_reads[2 * human_indices[i]] = human_reads[2 * human_indices[i]][:-4] + str(len(human_reads[2 * human_indices[i] + 1]) - 1) + '\n'


    with open(args.output_file, "w", encoding="utf-8") as fw:
        fw.write(''.join(human_reads))


def individual_contaminate():
    with open(args.human_file, "r", encoding="utf-8") as fr:
        human_reads = fr.readlines()
        total_length = (len("".join(human_reads[1::2])) - len(human_reads)) / 2

    with open(args.contaminate_file, "r", encoding="utf-8") as fr:
        contamination_reads = fr.readlines()


    number_contaminated_reads = int((total_length * args.contamination_rate) / (args.contamination_length * args.sequence_identity))
    human_indices = random.sample(range((len(human_reads)-1)//2), k=number_contaminated_reads)
    bacterial_indices = random.sample(range((len(contamination_reads)-1)//2), k=number_contaminated_reads)
    num_changes_per_read = int(args.sequence_identity * args.contamination_length)
    for i in range(number_contaminated_reads):

        # Get lines to contaminate
        contaminate_read = np.array(list(contamination_reads[2 * bacterial_indices[i] + 1]))
        human_read = np.array(list(human_reads[2 * human_indices[i] + 1]))

        # Find contamination_length window and choose random indices within it to replace at the sequence_identity rate
        starting_index = random.randint(0,len(contaminate_read) - args.contamination_length - 1)
        insertion_indices = random.sample(range(starting_index,starting_index + args.contamination_length), k=num_changes_per_read)


        # Set the randomly chosen human read to the randomly chosen bacterial read
        human_read[insertion_indices] = contaminate_read[insertion_indices]
        human_reads[2 * human_indices[i] + 1] = "".join(human_read)

        # Set human read title to have the correct line length
        human_reads[2 * human_indices[i]] = human_reads[2 * human_indices[i]][:-4] + str(len(human_reads[2 * human_indices[i] + 1]) - 1) + '\n'


    with open(args.output_file, "w", encoding="utf-8") as fw:
        fw.write(''.join(human_reads))

def main():
    if args.read_based:
        read_based_contaminate()
    else:
        individual_contaminate()

main()