"""
Required operations:

1.    get the number of vertices;
2.    parse (iterate) the set of vertices;
3.    given two vertices, find out whether there is an edge from the first one to the second one,
        and retrieve the Edge_id if there is an edge (the latter is not required if an edge is represented simply
        as a pair of vertex identifiers);
4.    get the in degree and the out degree of a specified vertex;
5.    parse (iterate) the set of outbound edges of a specified vertex (that is, provide an iterator).
        For each outbound edge, the iterator shall provide the Edge_id of the current edge
        (or the target vertex, if no Edge_id is used).
6.    parse the set of inbound edges of a specified vertex (as above);
7.    get the endpoints of an edge specified by an Edge_id (if applicable);
8.    retrieve or modify the information (the integer) attached to a specified edge.
9.    The graph shall be modifiable: it shall be possible to add and remove an edge, and to add and remove a vertex.
        Think about what should happen with the properties of existing edges and with the identification of remaining vertices.
        You may use an abstract Vertex_id instead of an int in order to identify vertices;
        in this case, provide a way of iterating the vertices of the graph.
10.   The graph shall be copyable, that is, it should be possible to make an exact copy of a graph,
        so that the original can be then modified independently of its copy.
        Think about the desirable behaviour of an Edge_property attached to the original graph, when a copy is made.

"""
from errors.exceptions import GraphError

from copy import deepcopy


class DirectedCostGraph:
    def __init__(self):
        """
            Creates a directed cost graph with 3 dictionaries that will be filled with data from the input file
        from the specified path

        dict_in -> dict that holds as key a vertex and as value a list of predecessor vertices
        dict_out -> dict that holds as key a vertex and as value a list of successor vertices
        dict_costs -> dict that holds as key a tuple containing the start and end of the edge and as value the edge's
                    cost
        """
        self.__dict_in = {}
        self.__dict_out = {}
        self.__dict_costs = {}

    def is_vertex(self, vertex):
        if vertex in self.__dict_in or vertex in self.__dict_out:
            return True
        return False

    def is_edge(self, edge_start, edge_end):
        """
        Checks whether there is an edge from the vertex "edge_start" to "edge_end"
        :return -> True if there is such an edge
                -> False if there is not
        """
        if not self.is_vertex(edge_start) or not self.is_vertex(edge_end):
            return False
        if edge_start not in self.__dict_in[edge_end]:
            return False
        if edge_end not in self.__dict_out[edge_start]:
            return False
        return True

    def add_vertex(self, new_vertex):
        """
        Adds a new vertex to the graph by modifying the in, out dictionaries to include a new key
        :return: True if operation was successful
                False if the vertex was already in the graph
        """
        if self.is_vertex(new_vertex):
            return False
        self.__dict_in[new_vertex] = []
        self.__dict_out[new_vertex] = []
        return True

    def add_edge(self, edge_start, edge_end, cost: int = 0):
        """
        Updates the in and out dictionaries of the vertices of the edge and adds a new edge to the cost dict
        :return: True if we managed to add a new edge
                False if the edge was already in the graph
                GraphError if the vertices are not in the graph.
        """
        if not self.is_vertex(edge_start) or not self.is_vertex(edge_end):
            raise GraphError("Vertex is not within the graph.")
        if self.is_edge(edge_start, edge_end):
            return False
        # Add predecessor
        self.__dict_in[edge_end].append(edge_start)
        # Add successor
        self.__dict_out[edge_start].append(edge_end)
        # Add cost
        self.__dict_costs[(edge_start, edge_end)] = cost
        return True

    def remove_vertex(self, vertex):
        """
        Modifies dict_in, dict_out, dict_costs such that the vertex is removed completely from the graph
        :return: False if operation was unsuccessful or if there is no such vertex
                True if we managed to remove the vertex and its side effects from the graph.
        """
        if not self.is_vertex(vertex):
            return False
        for predecessor in list(self.__dict_in[vertex]):
            self.remove_edge(predecessor, vertex)
        self.__dict_in.pop(vertex)
        for successor in list(self.__dict_out[vertex]):
            self.remove_edge(vertex, successor)
        self.__dict_out.pop(vertex)
        return True

    def remove_edge(self, edge_start, edge_end):
        """
        Modifies dict_in, dict_out, dict_costs such that the edge (edge_start, edge_end) is removed completely from the
        graph
        :param edge_start: the vertex where the edge starts
        :param edge_end: the vertex where the edge ends
        :return: False if the operation was unsuccessful or if there is no such edge
                True if dict_int, dict_out and dict_costs were successfully modified such that the specified edge is
                         no longer in the graph
        """
        if not self.is_edge(edge_start, edge_end):
            return False
        # if not edge_start in self.__dict_in[edge_end]:
        #     return False
        # if not edge_end in self.__dict_out[edge_start]:
        #     return False
        # if not (edge_start, edge_end) in self.__dict_costs.keys():
        #     return False
        self.__dict_in[edge_end].remove(edge_start)
        self.__dict_out[edge_start].remove(edge_end)
        self.__dict_costs.pop((edge_start, edge_end))
        return True

    def get_number_of_vertices(self):
        return len(self.__dict_in)

    def get_number_of_edges(self):
        return len(self.__dict_costs)

    def parse_all_vertices(self):
        return list(self.__dict_in.keys())

    def parse_all_edges(self):
        return list(self.__dict_costs.keys())

    def parse_out_vertices(self, start_vertex):
        return list(self.__dict_out[start_vertex])

    def parse_in_vertices(self, end_vertex):
        return list(self.__dict_in[end_vertex])

    def parse_out_edges(self, vertex):
        """
        function returns a list of tuples meaning the edges that are going out of the specified vertex
        raises GraphError if the vertex is not found in graph
        """
        if not self.is_vertex(vertex):
            raise GraphError("Vertex is not within the graph.")
        outbound_edges = []
        for successor in self.__dict_out[vertex]:
            outbound_edges.append((vertex, successor))
        return outbound_edges

    def parse_in_edges(self, vertex):
        """
            function returns the list of predecessors of the parameter "vertex" with the intent to be iterated upon
            raises GraphError if the vertex is not found in graph
        """
        if not self.is_vertex(vertex):
            raise GraphError("Vertex is not within the graph.")
        inbound_edges = []
        for predecessor in self.__dict_in[vertex]:
            inbound_edges.append((predecessor, vertex))
        return inbound_edges

    def get_in_degree(self, vertex):
        """
        :return: raises GraphError if vertex is not in graph
                else: returns the number of predecessors of vertex parameter
        """
        if not self.is_vertex(vertex):
            raise GraphError("Vertex is not within the graph.")
        return len(self.__dict_in[vertex])

    def get_out_degree(self, vertex):
        """
        :return: raises GraphError if vertex is not in graph
                else: returns the number of successors of vertex parameter
        """
        if not self.is_vertex(vertex):
            raise GraphError("Vertex is not within the graph.")
        return len(self.__dict_out[vertex])

    def get_edge_cost(self, edge_start, edge_end):
        if not self.is_edge(edge_start, edge_end):
            raise GraphError("Edge not in graph")
        return self.__dict_costs[(edge_start, edge_end)]

    def modify_edge_cost(self, edge_start, edge_end, new_cost: int = 0):
        """
        :return: raises GraphError if there is no such edge
                otherwise, modifies the cost of the edge indicated by the parameters
        """
        if not self.is_edge(edge_start, edge_end):
            raise GraphError(f'There is no edge from {edge_start} to {edge_end}')
        self.__dict_costs[(edge_start, edge_end)] = new_cost

    def get_copy(self):
        return deepcopy(self)

    def initialize_vertices(self, number_of_initial_vertices):
        for i in range(0, number_of_initial_vertices):
            self.__dict_in[i] = []
            self.__dict_out[i] = []


if __name__ == "__main__":
    graph = DirectedCostGraph()
    print(graph.get_number_of_vertices())
