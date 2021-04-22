import numpy as np 
import matplotlib.pyplot as plt
import argparse
from joblib import Parallel, delayed
from multiprocessing import cpu_count
import time


def go_roulette(capital, f):
    q = 9/19 #Probability of winning colour bet
    t = 60.0 # 1 spin every 60 seconds
    no_spins = 0.0
    while True:
        no_spins += 1.0
        capital = (1.0+f)*capital if np.random.rand() < q else (1.0-f)*capital
        if ( capital <= 10.0 or capital >= 2000.0 ) :
            break
    time = no_spins * 60.0

    return time

def main():
    #Initialise Variables
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_samples", "-n", help="Set the no. of identical samples / no. of times Andrew goes to roulette. Recommended: 10000+", type = int)
    parser.add_argument("--bin_size", "-b", help="Set the no. of bins for histogram. Recommended: 100-1000", type = int)
    args = parser.parse_args()
    no_samples = args.no_samples
    bin_size = args.bin_size

    #Run go_roulette in parallel no_samples many times, and return a list of waiting times with the same length
    start = time.time()
    times = Parallel(n_jobs=cpu_count())(delayed(go_roulette)(1000.0, 0.05) for _ in range(no_samples))
    end = time.time()


    #Results
    mean = np.mean(times)
    print("Average time spent in casino: {} seconds".format(mean))
    print("-----------------------------\
            \nTotal computation time: {}\
            \n-----------------------------".format(np.round(end-start))
            )
    weights = np.ones_like(times) / float(no_samples)
    plt.hist(times, bins=bin_size, weights = weights, label = "PDF", color = 'salmon')
    plt.legend(
            labels = ["no_samples: {:.1E}".format(no_samples), "Mean: {:.3E} seconds".format(mean)] ,
            fontsize= 'medium',
            loc = "upper right"
            )
    ax = plt.gca()
    ax.set_title(label='PDF of time spent in Casino', fontsize = 'x-large')
    ax.set_ylabel(ylabel = 'Fraction of samples', fontsize = 'large')
    ax.set_xlabel(xlabel='Time spent in Casino (seconds)', fontsize = "large" )
    plt.savefig("PDF_no_samples={:.1E}_bin_size={:.1E}.pdf".format(no_samples, bin_size))
    plt.show()

main()