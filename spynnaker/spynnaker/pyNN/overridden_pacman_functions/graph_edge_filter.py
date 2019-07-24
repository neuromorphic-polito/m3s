# pacman imports
from pacman.model.graphs.application.impl.application_edge \
    import ApplicationEdge
from pacman.model.graphs.machine.impl.machine_graph import MachineGraph
from pacman.model.graphs.common.graph_mapper import GraphMapper
from spinn_machine.utilities.progress_bar import ProgressBar

# spynnaker imports
from spynnaker.pyNN import exceptions
from spynnaker.pyNN.models.abstract_models.abstract_filterable_edge \
    import AbstractFilterableEdge

import logging
logger = logging.getLogger(__name__)


class GraphEdgeFilter(object):
    """ Removes graph edges that aren't required
    """

    def __call__(self, machine_graph, graph_mapper):
        """
        :param machine_graph: the machine_graph whose edges are to be filtered
        :param graph_mapper: the graph mapper between graphs
        :return: a new graph mapper and machine graph
        """
        new_machine_graph = MachineGraph(label=machine_graph.label)
        new_graph_mapper = GraphMapper()

        # create progress bar
        progress_bar = ProgressBar(
            len(machine_graph.vertices) + len(machine_graph.edges),
            "Filtering edges")

        # add the vertices directly, as they wont be pruned.
        for vertex in machine_graph.vertices:
            new_machine_graph.add_vertex(vertex)
            associated_vertex = graph_mapper.get_application_vertex(vertex)
            vertex_slice = graph_mapper.get_slice(vertex)
            new_graph_mapper.add_vertex_mapping(
                machine_vertex=vertex, vertex_slice=vertex_slice,
                application_vertex=associated_vertex)
            progress_bar.update()

        # start checking edges to decide which ones need pruning....
        for vertex in machine_graph.vertices:
            out_going_partitions = \
                machine_graph.get_outgoing_edge_partitions_starting_at_vertex(
                    vertex)
            for partition in out_going_partitions:
                for edge in partition.edges:
                    if not self._is_filterable(edge, graph_mapper):
                        logger.debug(
                            "this edge was not pruned {}".format(edge))
                        new_machine_graph.add_edge(edge, partition.identifier)
                        app_edge = graph_mapper.get_application_edge(edge)
                        new_graph_mapper.add_edge_mapping(edge, app_edge)
                    else:
                        logger.debug(
                            "this edge was pruned {}".format(edge))
                    progress_bar.update()
        progress_bar.end()

        # returned the pruned graph and graph_mapper
        return new_machine_graph, new_graph_mapper

    @staticmethod
    def _is_filterable(edge, graph_mapper):
        app_edge = graph_mapper.get_application_edge(edge)
        if isinstance(edge, AbstractFilterableEdge):
            return edge.filter_edge(graph_mapper)
        elif isinstance(app_edge, ApplicationEdge):
            return False
        else:
            raise exceptions.FilterableException(
                "cannot figure out if edge {} is prunable or not".format(edge))