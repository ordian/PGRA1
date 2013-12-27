#! /usr/bin/env python3
# coding=utf-8

import math

class Stats(object):
    @staticmethod
    def mean(l):
        return float(sum(l)) / len(l)

    @staticmethod
    def var(l):
        avg = Stats.mean(l);
        sum = 0.0;
        for a in l:
            sum += (a - avg) * (a - avg)
        return sum / (len(l) - 1)

    @staticmethod
    def stddev(l):
        return math.sqrt(Stats.var(l))

    @staticmethod
    def confidence(l):
        """
        (lower, upper) bound of the 95 percent confidence interval
        """
        avg = Stats.mean(l)
        stddev = Stats.stddev(l)
        dev = 1.96 * stddev / math.sqrt(len(l))
        return (avg - dev, avg + dev)
        