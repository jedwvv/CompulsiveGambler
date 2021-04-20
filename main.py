import numpy as np 
import matplotlib.pyplot as plt
import argparse
from joblib import Parallel, delayed
from multiprocessing import cpu_count
import time


def go_roulette(capital, f):
    q = 9/19
    t = 60
    no_spins = 0
    while True:
        no_spins += 1
        capital = (1+f)*capital if np.random.rand() < q else (1-f)*capital
        if ( capital <= float(10) or capital >= float(2000) ) :
            break
    time = no_spins * 60

    return time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_samples", "-n", help="Set the no. of identical samples / no. of times Andrew goes to roulette. Recommended: 10000+", type = int)
    args = parser.parse_args()
    no_samples = args.no_samples
    start = time.time()
    times = Parallel(n_jobs=cpu_count())(delayed(go_roulette)(1000, 0.05) for _ in range(no_samples))
    end = time.time()
    plt.hist(times, bins=1000)
    plt.show()
    print("Time taken: {}".format(np.round(end-start)))

main()