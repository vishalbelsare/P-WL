#!/usr/bin/env python3
#
# main.py: main script for testing Persistent Weisfeiler--Lehman graph
# kernels.


import igraph as ig

import argparse
import logging

from topology import PersistenceDiagramCalculator
from weight_assigner import WeightAssigner  # FIXME: put this in a different module
from WL import WL


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('FILES', nargs='+', help='Input graphs (in some supported format)')
    parser.add_argument('-n', '--num-iterations', default=3, type=int, help='Number of Weisfeiler-Lehman iterations')
    parser.add_argument('-f', '--filtration', type=str, default='sublevel', help='Filtration type')

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('P-WL')

    args = parser.parse_args()
    graphs = [ig.read(filename) for filename in args.FILES]

    logger.debug('Read {} graphs'.format(len(graphs)))

    wl = WL()
    wa = WeightAssigner()
    pdc = PersistenceDiagramCalculator()  # FIXME: need to add order/filtration

    for graph in graphs:
        wl.fit_transform(graph, args.num_iterations)

        # Stores the new multi-labels that occur in every iteration,
        # plus the original labels of the zeroth iteration.
        iteration_to_label = wl._multisets
        iteration_to_label[0] = wl._graphs[0].vs['label']

        total_persistence_values = []

        for iteration in sorted(iteration_to_label.keys()):
            graph.vs['label'] = iteration_to_label[iteration]
            graph = wa.fit_transform(graph)
            persistence_diagram = pdc.fit_transform(graph)

            total_persistence_values.append(persistence_diagram.total_persistence())

        print(total_persistence_values)
