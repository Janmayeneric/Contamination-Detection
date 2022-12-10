# Contamination-Detection

### Overview
An experiment conducted to evaluate a few algorithms for detecting DNA contamination in genetic samples. For a detailed description of the project, see [our paper](https://docs.google.com/document/d/1H0eskVyN2bw598BKahwPZZeatdrgg8UWtNJwoevdmlU/edit?usp=sharing)

### Synthetic Data
Test data was generated to analyse our algorithms, and it was modeled on real world contamination. For details on our research into modeling real world DNA contamination, see the Synthetic Contamination section of[our paper](https://docs.google.com/document/d/1H0eskVyN2bw598BKahwPZZeatdrgg8UWtNJwoevdmlU/edit?usp=sharing)

contaminate.py is the main file for generating test. You can tune the following parameters to create a synthetic contamination:
 - human_file = Intended fasta file
 - contaminate_file = Foreign DNA fasta file to contaminate human file
 - output_fil = Output file name
 - contamination_rate = The fraction of the overall template that was contaminated
 - sequence_identity = The fraction of each edit window that will be editted
 - contamination_length = The edit window length that edits will span
 - read_based = Replace human reads with contaminate reads vs individual bp contamination. Only uses contamination_rate if read based.



To generate the data used in our experiment, run the following commands:


##### verrying_contamination_length

python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=0 --contamination_rate=0.02 --output_file=synthetic_data/SRR6756023_CR=P02_SI=P25_CL=10.fastq --sequence_identity=0.25 --contamination_length=10
python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=0 --contamination_rate=0.02 --output_file=synthetic_data/SRR6756023_CR=P02_SI=P25_CL=20.fastq --sequence_identity=0.25 --contamination_length=20
python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=0 --contamination_rate=0.02 --output_file=synthetic_data/SRR6756023_CR=P02_SI=P25_CL=50.fastq --sequence_identity=0.25 --contamination_length=50


##### verrying_contamination_rate

python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=0 --contamination_rate=0.01 --output_file=synthetic_data/SRR6756023_CR=P01_SI=P75_CL=50.fastq --sequence_identity=0.75 --contamination_length=50
python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=0 --contamination_rate=0.02 --output_file=synthetic_data/SRR6756023_CR=P02_SI=P75_CL=50.fastq --sequence_identity=0.75 --contamination_length=50
python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=0 --contamination_rate=0.05 --output_file=synthetic_data/SRR6756023_CR=P05_SI=P75_CL=50.fastq --sequence_identity=0.75 --contamination_length=50
python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=0 --contamination_rate=0.10 --output_file=synthetic_data/SRR6756023_CR=P10_SI=P75_CL=50.fastq --sequence_identity=0.75 --contamination_length=50


##### verrying_sequence_identity

python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=0 --contamination_rate=0.02 --output_file=synthetic_data/SRR6756023_CR=P02_SI=P100_CL=50.fastq --sequence_identity=1.00 --contamination_length=50
python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=0 --contamination_rate=0.02 --output_file=synthetic_data/SRR6756023_CR=P02_SI=P75_CL=50.fastq --sequence_identity=0.75 --contamination_length=50
python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=0 --contamination_rate=0.02 --output_file=synthetic_data/SRR6756023_CR=P02_SI=P50_CL=50.fastq --sequence_identity=0.50 --contamination_length=50
python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=0 --contamination_rate=0.02 --output_file=synthetic_data/SRR6756023_CR=P02_SI=P25_CL=50.fastq --sequence_identity=0.25 --contamination_length=50


##### whole_reads

python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=1 --output_file=synthetic_data/SRR6756023_p01_reads.fastq --contamination_rate=0.01
python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=1 --output_file=synthetic_data/SRR6756023_p02_reads.fastq --contamination_rate=0.02
python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=1 --output_file=synthetic_data/SRR6756023_p05_reads.fastq --contamination_rate=0.05
python contaminate.py --human_file=raw_data/SRR6756023_200_reads.fasta --contaminate_file=raw_data/staphylococcus.fasta  --read_based=1 --output_file=synthetic_data/SRR6756023_p10_reads.fastq --contamination_rate=0.10
