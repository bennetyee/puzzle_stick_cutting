#!/usr/bin/python3

import argparse
import random
import sys

# Textual "plot" for now
# import matplotlib.pyplot as plt
# import numpy as np

Debug=False

def SatisfiesTriangleInequality(s0, s1, s2):
    sticks = [s0, s1, s2]
    sticks.sort()
    return (sticks[0] + sticks[1] >= sticks[2] and
            sticks[0] + sticks[2] >= sticks[1] and
            sticks[1] + sticks[2] >= sticks[0])

def CanMakeTriangleWithCuts(cut0, cut1):
    if cut0 > cut1:
        t = cut0
        cut0 = cut1
        cut1 = t
    # 0 <= cut0 <= cut1 <= 1.0

    s0 = cut0
    s1 = cut1 - cut0
    s2 = 1.0 - cut1

    if Debug:
        sys.stdout.write('cuts    %f, %f; ' % (cut0, cut1))
        sys.stdout.write('lengths %f, %f, %f: ' % (s0, s1, s2))

    can_form_triangle = SatisfiesTriangleInequality(s0, s1, s2)
    if Debug:
        sys.stdout.write('%s\n' % str(can_form_triangle))
    return can_form_triangle

def RunOneExperiment(rng):
    cut0 = rng.random()
    cut1 = rng.random()
    return CanMakeTriangleWithCuts(cut0, cut1)

def RunManyExperiments(rng, how_many):
    num_triangles = sum([1 for _ in range(how_many) if RunOneExperiment(rng)])
    return num_triangles / how_many

def StateSpace(incr):
    scale=int(1.0/incr)
    for cut1 in range(0, scale):
        for cut2 in range(0, scale):
            if CanMakeTriangleWithCuts(float(cut1)/scale, float(cut2)/scale):
                sys.stdout.write('*')
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true',
                        help='generate debugging output')
    parser.add_argument('--num-samples', '-n', default=10000, type=int,
                        help='the number of Monte Carlo experiments to run')
    parser.add_argument('--mode', '-m', choices=['monte_carlo', 'state_space'],
                        default='monte_carlo',
                        help='either monte_carlo experiment, or state space plot')
    parser.add_argument('--increment', '-i', default=0.01, type=float,
                        help='state space plot increment')
    parser.add_argument('--seed', default=None, type=int,
                        help='seed for rng')
    ns = parser.parse_args(args)
    global Debug
    Debug = ns.debug
    if ns.mode == 'monte_carlo':
        sys.stdout.write('%f\n' % RunManyExperiments(random.Random(ns.seed), ns.num_samples))
    else:
        StateSpace(ns.increment)

if __name__ == '__main__':
    main(sys.argv[1:])
