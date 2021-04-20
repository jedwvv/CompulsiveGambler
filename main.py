import numpy as np 
import matplotlib.pyplot as plt
import argparse
from joblib import Parallel, delayed
from multiprocessing import cpu_count
import time


def go_roulette(capital, f):
    q = 9/19 #Probability of winning colour bet
    t = 60 # 1 spin every 60 seconds
    no_spins = 0 
    while True:
        no_spins += 1
        capital = (1+f)*capital if np.random.rand() < q else (1-f)*capital
        if ( capital <= float(10) or capital >= float(2000) ) :
            break
    time = no_spins * 60

    return time

def main():
    #Initialise Variables
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_samples", "-n", help="Set the no. of identical samples / no. of times Andrew goes to roulette. Recommended: 10000+", type = int)
    args = parser.parse_args()
    no_samples = args.no_samples

    #Run go_roulette in parallel no_samples many times, and return a list of waiting times with the same length
    start = time.time()
    times = Parallel(n_jobs=cpu_count())(delayed(go_roulette)(1000, 0.05) for _ in range(no_samples))
    end = time.time()

    #Results
    print("Average time spent in casino: {} seconds".format(np.mean(times)))
    print("-----------------------------\
            \nTotal computation time: {}\
            \n-----------------------------".format(np.round(end-start))
            )
    plt.hist(times, bins=1000)
    plt.show()

main()