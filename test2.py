from random import random
import statistics
from collections import Counter
import pandas
import matplotlib.pyplot as plt

a_list = []

def Run(input):
    n = 0
    c = 0
    c_list = []

    while (n < 100000):
        result = input
        while(result > 0):
            result = round(random() * result)
            c+=1
        c_list.append(c)
        c = 0
        n+=1
    print("For !roll", input)
    #print("Mean: ", statistics.mean(c_list))
    #print("Mode: ", statistics.mode(c_list))
    return statistics.mean(c_list)
    #count = Counter(c_list)
    #df = pandas.DataFrame.from_dict(count, orient='index').sort_index()
    #df.plot(kind='bar')
    #plt.show()

x = 2
while x < 1000000000000:
    result = [x,Run(x)]
    print(result)
    a_list.append(result)
    x = round(x * 1.44 )
    

print(a_list)
plt.plot(*zip(*a_list))
plt.xscale('log')
plt.show()