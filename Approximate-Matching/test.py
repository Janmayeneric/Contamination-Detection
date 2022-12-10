
from match import EditDistance

from time import time

import matplotlib.pyplot as plt

t_list = []
s_list = []
for i in [1000,2500,5000,7500,10000]:
    s = 'a' * i
    start = time()
    ed = EditDistance(s, s)
    ed.match()
    print(ed.min_edit)
    t_list.append(time() - start)
    s_list.append(i)

plt.plot(s_list,t_list)
plt.ylabel('time(second)')
plt.xlabel('n length p to n length t matching')
plt.show()






