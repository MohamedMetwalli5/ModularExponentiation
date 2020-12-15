import time
from matplotlib import pyplot as plt
import random

def naive1(b,n,m):
    b = b-1
    start = time.perf_counter_ns()
    r = 1
    for i in range(n):
        if r > ((2**31)-1):
           #print("naive1 over flow at bits" ,len(bin(b)[2:]) , r)
           return [r,0]
        r = r*b
    r = r%m
    stop = time.perf_counter_ns()
    period = stop - start
    return [r,period]


def naive2(b,n,m):
    b = b-1
    start = time.perf_counter_ns()
    r = 1
    for i in range(n):
        r = (r * b)
        if r > ((2**31)-1):
           #print("naive2 over flow at bits" ,len(bin(b)[2:]))
           return [r,0]
        r = r % m
    stop = time.perf_counter_ns()
    period = stop - start
    return [r, period]



def FastExponentiationIterative(b,n,m):
    r = 1
    start = time.perf_counter_ns()
    while n > 0:
        if n%2 == 0:
            b = (b*b)
            if b > (2**32)-1 :
                return[r,0]
            b %= m
            n /= 2
        else:
            r = (r*b)
            if r > (2**32)-1 :
                return[r,0]
            r %= n
            n -= 1
    stop = time.perf_counter_ns()
    period = stop - start
    return [r,period]

def FastExponentiationRecursive(b,n,m):
    if n == 0:
        return 1
    elif n%2 == 0:
        flag = b*b
        if flag > ((2 ** 32) - 1):
            return 0
        else:
            return FastExponentiationRecursive((b*b)%m,n/2,m)
    elif n%2 != 0:
        flag = (b * FastExponentiationRecursive(b, n-1, m))
        if flag > ((2 ** 32) - 1):
            return 0
        else :
            return (b * FastExponentiationRecursive(b, n-1, m)) % m

def FastExponentiationRecursiveTimer(b,n,m):
    start = time.perf_counter_ns()
    result = FastExponentiationRecursive(b,n,m)
    stop = time.perf_counter_ns()
    period = stop - start
    return [result,period]

if __name__ == '__main__':
    timesNaive1 = []
    timesNaive2 = []
    timeFastIterative = []
    timeFastRecursive = []

    for i in range (1,32):
        timesNaive1.append(0)
        timesNaive2.append(0)
        timeFastIterative.append(0)
        timeFastRecursive.append(0)
        for j in range (20):
            number = random.getrandbits(i)
            resultNaive1 = naive1((int(number)+1), (int(number)+1), (int(number)+1))
            resultNaive2 = naive2((int(number)+1), (int(number)+1), (int(number)+1))
            resultFastIterative = FastExponentiationIterative((int(number)+1), (int(number)+1), (int(number)+1))
            resultFastRecursive = FastExponentiationRecursiveTimer((int(number)+1), (int(number)+1), (int(number)+1))

            timesNaive1[i-1] += resultNaive1[1]
            timesNaive2[i-1] += resultNaive2[1]
            timeFastIterative[i-1] += resultFastIterative[1]
            timeFastRecursive[i-1] += resultFastRecursive[1]

        timesNaive1[i-1] /= 20
        timesNaive2[i-1] /= 20
        timeFastIterative[i-1] /= 20
        timeFastRecursive[i-1] /= 10
    timesNaive1 = [item for item in (timesNaive1) if item > 0]
    timesNaive2 = [item for item in (timesNaive2) if item > 0]
    timeFastIterative = [item for item in (timeFastIterative) if item > 0]
    timeFastRecursive = [item for item in (timeFastRecursive) if item > 0]
    print(timesNaive1)
    print(timesNaive2)
    print(timeFastIterative)
    print(timeFastRecursive)
    print("finished")

    plt.figure(1)
    x = [i for i in range(5)]
    plt.plot(x , timesNaive1[1:6])
    plt.title("First naive method")
    plt.xlabel("Number of bits")
    plt.ylabel("Time")

    plt.figure(2)
    x = [i for i in range(len([item for item in (timesNaive2) if item > 0]))]
    plt.plot(x , [item for item in (timesNaive2) if item > 0])
    plt.title("Second naive method")
    plt.xlabel("Number of bits")
    plt.ylabel("Time")

    plt.figure(3)
    x = [i for i in range(len([item for item in (timeFastIterative) if item > 0]))]
    plt.plot(x, [item for item in (timeFastIterative) if item > 0])
    plt.title("Fast (iterative method)")
    plt.xlabel("Number of bits")
    plt.ylabel("Time")

    plt.figure(4)
    x = [i for i in range(len([item for item in (timeFastRecursive) if item > 0]))]
    plt.plot(x, [item for item in (timeFastRecursive) if item > 0])
    plt.title("Fast (recursive method)")
    plt.xlabel("Number of bits")
    plt.ylabel("Time")
    plt.show()
