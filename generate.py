#! /usr/bin/env python

import sys
import networkx as nx
import random


def start_cost_function(degree):
    return degree

def random_edge_cost():
    if random.random() < 0.8:
        return 10
    return 30

class Task(object):
    def __init__(self, num_nodes, num_start, num_end, num_poi, discard_cost, start_cost, edge_cost):
        self.discard_cost = discard_cost
        self.start_cost_function = start_cost
        self.edge_cost_function = edge_cost
        self.graph = self.generate_connected_graph(num_nodes)
        self.poi = self.generate_poi(num_poi)
        self.end = self.generate_end_nodes(num_end)
        self.start = self.generate_start_nodes(num_start)


    def generate_directed_graph(self, num_nodes):
        # return nx.gn_graph(num_nodes)
        graph = nx.barabasi_albert_graph(num_nodes, 2)

        directed = graph.to_directed()
        for s, t in graph.edges():
            if random.random() < 0.01:
                continue
            if random.random() < 0.5:
                directed.remove_edge(s,t)
            else:
                directed.remove_edge(t,s)

        return directed


    def generate_connected_graph(self, num_nodes):
        is_connected = False
        while not is_connected:
            graph = self.generate_directed_graph(num_nodes)
            is_connected = nx.is_weakly_connected(graph)

        return graph

    def generate_poi(self, num_poi):
        return random.sample(self.graph.nodes(), num_poi)

    def generate_start_nodes(self, num_nodes):
        startnodes = [ (n, 0) for n, degree in self.graph.in_degree(self.graph.nodes()) if degree == 0]
        nonstartnodes = [ n for n, degree in self.graph.in_degree(self.graph.nodes()) if degree > 0]
        if len(startnodes) >= num_nodes:
            return random.sample(startnodes, num_nodes)
        num_remaining_nodes = num_nodes - len(startnodes)
        remaining_nodes = random.sample(nonstartnodes, num_remaining_nodes)
        remaining_nodes_with_cost = [ (n, self.start_cost_function(degree)) for n, degree in self.graph.in_degree(remaining_nodes)]
        startnodes.extend(remaining_nodes_with_cost)
        return startnodes

    def generate_end_nodes(self, num_nodes):
        endnodes = [ n for n, degree in self.graph.out_degree(self.graph.nodes()) if degree == 0]
        nonendnodes = [ n for n, degree in self.graph.out_degree(self.graph.nodes()) if degree > 0]
        if len(endnodes) >= num_nodes:
            return random.sample(endnodes, num_nodes)
        num_remaining_nodes = num_nodes - len(endnodes)

        endnodes.extend(random.sample(nonendnodes, num_remaining_nodes))
        return endnodes

    def _write_costs(self, fh):
        fh.write("        (= (total-cost) 0)\n")
        fh.write("        (= (discard-cost) %s)\n" % self.discard_cost)
        for s, cost in self.start:
            fh.write("        (= (starting-cost o%s) %s)\n" % (s, cost))

        for s, d in self.graph.edges():
            fh.write("        (= (connected-cost o%s o%s) %s)\n" % (s,d, self.edge_cost_function()))


    def _write_static(self, fh):
        for s, _ in self.start:
            fh.write("        (SOURCE o%s)\n" % s)

        for s in self.end:
            fh.write("        (TARGET o%s)\n" % s)

        for s in self.poi:
            fh.write("        (POI o%s)\n" % s)

        for s, d in self.graph.edges():
            fh.write("        (CONNECTED o%s o%s)\n" % (s,d))

        last_discard = "dummy"
        for s in self.poi:
            curr = "o%s" % s
            fh.write("        (DISCARD_AFTER %s %s)\n" % (curr, last_discard))
            last_discard = curr

    def write_pddl(self, filename, domain_name, problem_name):
        with open(filename, "w") as f:
            f.write("(define (problem %s)\n" % problem_name)
            f.write("    (:domain %s)\n" % domain_name)
            f.write("    (:objects %s dummy)\n" % " ".join(["o%s" %s for s in self.graph.nodes()]))
            f.write("    (:init\n")

            self._write_static(f)
            self._write_costs(f)

            f.write("        (considered dummy)\n")

            f.write("    )\n")
            f.write("    (:goal (and\n")
            f.write("        (__goal-achieved)\n")
            for s in self.poi:
                f.write("        (considered o%s)\n" % s)  
            f.write("        )\n")
            f.write("    )\n")
            f.write("    (:metric minimize (total-cost))\n")
            f.write(")\n")

def main(prefix):
    # 
    counter = 1
    for num_nodes in [1000, 2500, 5000, 10000, 20000]:
        for start in [2, 5]:
            for end in [10, 100]:
                for pois in [3, 5, 10, 25, 50]:
                    task = Task(num_nodes, start, end, pois, 100, start_cost_function,random_edge_cost)
                    prob_name = "rm-%s-%s-%s-%s" % (num_nodes, start, end, pois)
                    fname = "%s%03d.pddl" % (prefix, counter)
                    print("Generating task: %s" % fname)          
                    task.write_pddl(fname, "risk", prob_name)
                    counter += 1

if __name__ == "__main__":
    main(sys.argv[1])
    