#! /usr/bin/env python3
# coding=utf-8

from graph_tool.all import *
import random
from UnionFind import UnionFind as UF
from Stats import Stats

class Percolation(object):

    def __init__(self, L, R, N, OUTPUT, IMAGE_SIZE):
        self.L = L
        self.R = R
        self.N = N
        self.OUTPUT = OUTPUT
        self.IMAGE_SIZE = IMAGE_SIZE
        self._graph_init()
        self.tests = []

    def _graph_init(self):
        self.g = Graph(directed=True)
        self.pos = self.g.new_vertex_property("vector<double>")
        self.vertices_color = self.g.new_vertex_property("vector<double>")
        self.edge_color = self.g.new_edge_property("vector<double>")
        self.pen = self.g.new_edge_property("double")
        self.vertices = []

        for v in range(self.L * self.L):
            self.vertices.append(self.g.add_vertex())
            current_vertice = self.g.vertex(v)
            self.pos[current_vertice] = self._get_pos(v)
            self.vertices_color[current_vertice] = [0.5, 0.5, 0.5, 1]

        
    def _get_pos(self, a):
        return (a // self.L, a % self.L)

    def _sqrdist(self, a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    def run(self):
        L = self.L
        R = self.R
        percolates = False

        union = UF(L * L + 2)
        # bottom
        for i in range(1, L + 1):
            union.union(i, 0)
        # top
        for i in range(L * L - L + 1, L * L + 1):
            union.union(i, L * L + 1)

        particles = set()
        edges     = set()

        while len(particles) != self.N:
            if percolates: break
            p = random.randrange(L, L * L - L)
            particles.add(p)
            current_vertice = self.g.vertex(p)
            self.vertices_color[current_vertice] = [0, 1, 0, 1]
            x, y = self._get_pos(p)
            for i in range(max(0, x - R), min(L, x + R + 1)):
                if percolates: break
                for j in range(max(0, y - R), min(L, y + R + 1)):
                    if (i, j) == (x, y): continue
                    if self._sqrdist((i, j), (x, y)) > R * R: continue
                    if i <= x: 
                        from_, to_ = i * L + j, p
                    else: 
                        from_, to_ = p, i * L + j
                    if i * L + j in particles or i == 0 or i == L - 1:
                        union.union(from_ + 1, to_ + 1)
                        edges.add((from_, to_))
                    if union.connected(L * L + 1, 0): 
                        percolates = True


        for edge in edges:
            if union.connected(0, edge[0] + 1):
                current_edge = self.g.add_edge(self.vertices[edge[0]], self.vertices[edge[1]])
                self.pen[current_edge] = 3
                if percolates:
                    self.edge_color[current_edge] = [0, 0, 1, 1]
                else:
                    self.edge_color[current_edge] = [1, 0, 0, 1]

        if percolates:
            self.tests.append(len(particles))

        return percolates

    def draw(self):
        graph_draw(self.g, pos = self.pos, edge_color = self.edge_color, edge_pen_width = self.pen, vertex_fill_color = self.vertices_color, output = self.OUTPUT, output_size = self.IMAGE_SIZE)


from optparse import OptionParser

if __name__=="__main__":
    parser = OptionParser()
    usage = "Usage: ./Percolation.py -L 100 -R 2 -N 500 -I 1000 -O out.png -T 100"
    parser.add_option("-L", "--Length", type="int",
              help="Grid side",
              dest="L", default=20)
    parser.add_option("-R", "--Limit", type="int",
              help="Limit distance", 
              dest="R", default=2)
    parser.add_option("-N", "--Number", type="int",
              help="Number of particles", 
              dest="N", default=500)
    parser.add_option("-I", "--Image", type="int",
              help="Image size", 
              dest="I", default=1000)
    parser.add_option("-O", "--Output", type="string",
              help="Output filename", 
              dest="O", default="out.png")
    parser.add_option("-T", "--Tests", type="int",
              help="Number of tests", 
              dest="T", default=50)
    (options, args) = parser.parse_args()
    
    p = Percolation(options.L, options.R, options.N, options.O, (options.I, options.I))
    print(p.run())
    p.draw()

    if options.T:
        p.N = options.L * options.L
        for _ in range(options.T):
            p.run()

        tests = sorted(p.tests)

        pace = max(options.T // 100, 1)
        stats = {}
        for i in range(0, options.T, pace):
            stats[tests[i]] = float(i) / options.T

        l = list(zip(*list(stats.items())))

        import matplotlib.pyplot as plt

        plt.plot(l[0], l[1], 'ro')
        plt.axis([0, options.L * options.L, 0, 1])
        plt.show()
        print("Mean: ", Stats.mean(l[0]))
        print("Deviation: ", Stats.stddev(l[0]))
        print("95 percent confidence interval: ", Stats.confidence(l[0]))
