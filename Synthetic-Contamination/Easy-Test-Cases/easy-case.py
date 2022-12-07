# For generating easy synthetic data samples with know contamination for testing

import random

bases = ['A','C','T','G']
template = random.choices(bases, k=10000)
pattern = template[3000:4000]
rand_list = random.sample(range(len(pattern)), k=30)
for i in rand_list:
    new_base = random.sample(bases,k=1)[0]
    while (new_base == pattern[i]):
        new_base = random.sample(bases,k=1)[0]
    pattern[i] = new_base

with open('template2-len=10000.txt','w') as wf:
    wf.write(''.join(template))

with open('pattern2-len=1000-ed=30.txt','w') as wf:
    wf.write(''.join(pattern))