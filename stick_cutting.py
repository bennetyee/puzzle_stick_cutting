#!/usr/bin/python3

import argparse
import math
import random
import subprocess
import sys

# Textual "plot" for now
# import matplotlib.pyplot as plt
# import numpy as np

Debug=False

def SatisfiesTriangleInequality(s0, s1, s2):
    sticks = [s0, s1, s2]
    sticks.sort()
    return (sticks[0] + sticks[1] > sticks[2] and
            sticks[0] + sticks[2] > sticks[1] and
            sticks[1] + sticks[2] > sticks[0])

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

# For this to be useful with a small increment, the terminal emulator
# should be set to use a small font and large number of rows and
# columns.
def StateSpace(incr):
    scale=int(1.0/incr)
    for cut1 in range(scale, -1, -1):
        ylabel='%4.2f' % (float(cut1)/scale)
        if ylabel[-1] == '0':
            sys.stdout.write('%3s ' % ylabel[:3])
        else:
            sys.stdout.write(' ' * 4)

        for cut2 in range(0, scale+1):
            if CanMakeTriangleWithCuts(float(cut1)/scale, float(cut2)/scale):
                sys.stdout.write('*')
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')
    sys.stdout.write('\n')
    for ch in range(3):
        sys.stdout.write(' ' * 4)
        for cut2 in range(0, scale+1):
            xlabel='%4.2f' % (float(cut2)/scale)
            if xlabel[-1] == '0':
                sys.stdout.write(xlabel[ch])
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')

def main(argv):
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
    parser.add_argument('--raw', action='store_true',
                        help='generate state_space output without spawning a window')
    parser.add_argument('--wait', action='store_true',
                        help='wait for a newline before exiting')
    parser.add_argument('--font', default='-*-fixed-*-*-*-*-*-100-*-*-*-*-*-*',
                        type=str,
                        help='xterm font to use')
    ns = parser.parse_args(argv[1:])
    global Debug
    Debug = ns.debug
    if ns.mode == 'monte_carlo':
        sys.stdout.write('%f\n' % RunManyExperiments(random.Random(ns.seed), ns.num_samples))
    else:
        if ns.raw:
            StateSpace(ns.increment)
        else:
            # 10 is "slop".  we need ~4 for axis labels.
            num_iter = math.ceil(1.0 / ns.increment) + 10
            size='%dx%d' % (num_iter, num_iter)
            try:
                completed = subprocess.run(['xterm', '-geom', size, '-fn', ns.font, '-e', argv[0], '--mode', 'state_space', '--increment', str(ns.increment), '--raw', '--wait'])
            except FileNotFoundError as e:
                sys.stderr.write('Error %s\n' % e)
                sys.stderr.write('Error running xterm. Please ensure it has been install (apt install xterm)\n')
    if ns.wait:
        input('Hit ENTER to close: ')

if __name__ == '__main__':
    main(sys.argv)
