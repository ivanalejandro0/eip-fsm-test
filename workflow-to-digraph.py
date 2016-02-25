#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Graph XWorkflows using dot language.

References:
https://github.com/rbarrois/django_xworkflows/pull/16/files
https://github.com/kmmbvnr/django-fsm
"""

from __future__ import unicode_literals

import graphviz


def workflow_to_digraph(name, workflow):
    """
    Generate a `graphviz.Digraph` from a `xworkflows.Workflow`.

    :param workflow: workflows to generate the digraph from
    :type workflows: xworkflows.Workflow

    :returns: a dot digraph
    :rtype: graphviz.Digraph
    """
    sources, targets, edges = set(), set(), set()

    # dump nodes and edges
    for transition in workflow.transitions._transitions.values():
        for source in transition.source:
            source_name = '%s.%s' % (name, source)
            target_name = '%s.%s' % (name, transition.target)
            sources.add((source_name, str(source)))
            targets.add((target_name, str(transition.target)))
            edges.add((source_name, target_name,
                       (('label', str(transition.name)),)))

    # construct subgraph
    subgraph = graphviz.Digraph(
        name="cluster_%s" % (name, ),
        graph_attr={
            'label': "%s" % (name, ),
            'labelloc': 'top',
            'labeljust': 'left',
        },
    )

    final_states = targets - sources
    for name, label in final_states:
        subgraph.node(name, label=label, shape='doublecircle')

    for name, label in (sources | targets) - final_states:
        label = label.replace('_', '\n')  # XXX hack to avoid lenghty names

        # HACK customize some states with specific colors
        if label == 'on':
            subgraph.node(name, label=label, shape='doublecircle',
                          fillcolor='palegreen', style='filled')
        elif label == 'error':
            subgraph.node(name, label=label, shape='doublecircle',
                          fillcolor='red', style='filled')
        elif label == 'off':
            subgraph.node(name, label=label, shape='doublecircle',
                          style='filled')
        else:
            # "normal" state
            subgraph.node(name, label=label, shape='circle')

        if workflow.initial_state:  # Adding initial state notation
            if label == workflow.initial_state:
                subgraph.node('.', shape='point')
                subgraph.edge('.', name)

    for source_name, target_name, attrs in edges:
        subgraph.edge(source_name, target_name, **dict(attrs))

    return subgraph


def generate_dot(workflows):
    """
    Generate a `graphviz.Digraph` from a `xworkflows.Workflow`.

    :param workflows: a list of workflows to generate the digraph from
    :type workflows: list of xworkflows.Workflow objects

    :returns: a dot digraph
    :rtype: graphviz.Digraph
    """
    # create main Digraph
    result = graphviz.Digraph()
    result.graph_attr['rankdir'] = 'LR'

    for name, workflow in workflows:
        subgraph = workflow_to_digraph(name, workflow)
        result.subgraph(subgraph)

    return result


# from eip.eip_machine import EIPWorkflow
from eip.firewall.workflow import FirewallWorkflow
from eip.vpn.workflow import VPNWorkflow


def main():
    workflows = {
        # 'eip (vpn+firewall)': EIPWorkflow,
        'vpn': VPNWorkflow,
        'firewall': FirewallWorkflow
    }

    dotdata = generate_dot(workflows.items())

    def render_output(graph):
        filename, format = 'graphs', 'png'

        graph.engine = 'dot'
        graph.format = format
        graph.render(filename)

    # print dotdata
    render_output(dotdata)


if __name__ == "__main__":
    main()
