#! /usr/bin/env python3
# coding=utf-8

from graph_tool.all import *
import random
from UnionFind import UnionFind as UF
from Stats import Stats

class Percolation(object):

    IMAGE_SIZE = (1000, 1000)
    OUTPUT = "out.png"

    def __init__(self, L, R, N):
        self.L = L
        self.R = R
        self.N = N
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
            self.vertices_color[current_vertice] = [1, 0, 0, 1]
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
                self.edge_color[current_edge] = [0, 0, 1, 1]

        if percolates:
            self.tests.append(len(particles))

        return percolates

    def draw(self):
        graph_draw(self.g, pos = self.pos, edge_color = self.edge_color, edge_pen_width = self.pen, vertex_fill_color = self.vertices_color, output = Percolation.OUTPUT, output_size = Percolation.IMAGE_SIZE)


from sys import argv

if __name__=="__main__":
    try:
        arguments = list(map(int, argv[1:]))
        L = arguments[0]
        assert(L > 1)
        R = arguments[1]
        assert(R > 0)
        N = arguments[2]
        assert(N > 0)
        NUM_TESTS = None
        if len(arguments) == 4:
            NUM_TESTS = arguments[3]
        OK = True
    except:
        print("""Usage: ./Percolation.py L R N
        Output: {0.OUTPUT}
        Image size: {0.IMAGE_SIZE[0]:d} X {0.IMAGE_SIZE[1]:d}""".format(Percolation))
        OK = None
    if OK:
        p = Percolation(L, R, N)
        print(p.run())
        p.draw()

        if NUM_TESTS:
            p.N = L * L
            for _ in range(NUM_TESTS):
                p.run()

            tests = sorted(p.tests)

            pace = max(NUM_TESTS // 100, 1)
            stats = {}
            for i in range(0, NUM_TESTS, pace):
                stats[tests[i]] = float(i) / NUM_TESTS

            l = list(zip(*list(stats.items())))

            import matplotlib.pyplot as plt

            plt.plot(l[0], l[1], 'ro')
            plt.axis([0, L * L, 0, 1])
            plt.show()
            print("Mean: ", Stats.mean(l[0]))
            print("Deviation: ", Stats.stddev(l[0]))
            print("95 percent confidence interval: ", Stats.confidence(l[0]))
