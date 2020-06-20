#!/usr/bin/python3

import argparse
import math
import random
import subprocess
import sys

import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

options=None

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

    if options.debug:
        sys.stdout.write('cuts    %f, %f; ' % (cut0, cut1))
        sys.stdout.write('lengths %f, %f, %f: ' % (s0, s1, s2))

    can_form_triangle = SatisfiesTriangleInequality(s0, s1, s2)
    if options.debug:
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
def TextStateSpace(incr):
    scale = int(1.0/incr)
    threshold = 1.0
    yincr = 0.1
    for cut1 in range(scale, -1, -1):
        yvalue = float(cut1) / scale
        ylabel='%3.1f' % yvalue
        if yvalue < threshold:
            threshold = threshold - yincr
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
        threshold = 0.0
        xincr = 0.1
        sys.stdout.write(' ' * 4)
        for cut2 in range(0, scale+1):
            xvalue = float(cut2) / scale
            xlabel='%3.1f' % xvalue
            if xvalue >= threshold:
                threshold = threshold + xincr
                sys.stdout.write(xlabel[ch])
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')

def PlotStateSpace(incr):
    scale = int(1.0 / incr)
    xs = []
    ys = []
    for x in range(0, scale+1):
        xf = float(x)/scale
        for y in range(0, scale+1):
            yf = float(y)/scale
            if CanMakeTriangleWithCuts(xf, yf):
                xs.append(xf)
                ys.append(yf)
    plt.figure()
    plt.clf()
    plt.axes(aspect='equal')
    plt.title('Can A Triangle Be Formed?')
    plt.scatter(xs, ys, 1, marker=',')
    plt.xlabel('Position of first cut')
    plt.ylabel('Position of second cut')
    if options.file is not None:
        plt.savefig(options.file)
    else:
        plt.show()

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true',
                        help='generate debugging output')
    parser.add_argument('--num-samples', '-n', default=10000, type=int,
                        help='the number of Monte Carlo experiments to run')
    parser.add_argument('--mode', '-m', choices=['monte_carlo', 'state_space', 'text_state_space'],
                        default='monte_carlo',
                        help='run a monte_carlo experiment, or generate state space plot (or text-mode "plot")')
    parser.add_argument('--file', default=None, type=str,
                        help='Generate output in <filename> when in state_space mode; use pdf, svg, pnf suffix to specify file format')
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
    global options
    options = parser.parse_args(argv[1:])
    if options.mode == 'monte_carlo':
        sys.stdout.write('%f\n' % RunManyExperiments(random.Random(options.seed), options.num_samples))
    elif options.mode == 'text_state_space':
        if options.raw:
            TextStateSpace(options.increment)
        else:
            # 10 is "slop".  we need ~4 for axis labels.
            num_iter = math.ceil(1.0 / options.increment) + 10
            size='%dx%d' % (num_iter, num_iter)
            try:
                completed = subprocess.run(['xterm', '-geom', size, '-fn', options.font, '-e', argv[0], '--mode', 'text_state_space', '--increment', str(options.increment), '--raw', '--wait'])
            except FileNotFoundError as e:
                sys.stderr.write('Error %s\n' % e)
                sys.stderr.write('Error running xterm. Please ensure it has been install (apt install xterm)\n')
        if options.wait:
            input('Hit ENTER to close: ')
    else:
        PlotStateSpace(options.increment)

if __name__ == '__main__':
    main(sys.argv)
