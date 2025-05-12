"""
11.   Read the graph from a text file (as an external function); see the format below.
12.   Write the graph from a text file (as an external function); see the format below.
13.   Create a random graph with specified number of vertices and of edges (as an external function).
"""
import random

from domain.graph import DirectedCostGraph
from collections import deque


class GraphController:
    def __init__(self, graph: DirectedCostGraph):
        self.__graph = graph
        self.__last_copy = self.__graph
        self.__graph_is_undirected = False

    def get_number_of_vertices(self) -> int:
        return self.__graph.get_number_of_vertices()

    def get_number_of_edges(self) -> int:
        if self.__graph_is_undirected:
            return self.__graph.get_number_of_edges() // 2
        return self.__graph.get_number_of_edges()

    def get_all_vertices(self) -> list:
        return self.__graph.parse_all_vertices()

    def check_if_edge(self, edge_start, edge_end) -> bool:
        return self.__graph.is_edge(edge_start, edge_end)

    def get_in_degree(self, vertex) -> int:
        return self.__graph.get_in_degree(vertex)

    def get_out_degree(self, vertex) -> int:
        return self.__graph.get_out_degree(vertex)

    def get_outbound_edges(self, vertex) -> list:
        return self.__graph.parse_out_edges(vertex)

    def get_inbound_edges(self, vertex) -> list:
        return self.__graph.parse_in_edges(vertex)

    def modify_cost(self, edge_start, edge_end, new_cost):
        return self.__graph.modify_edge_cost(edge_start, edge_end, new_cost)

    def get_edge_cost(self, edge_start, edge_end):
        return self.__graph.get_edge_cost(edge_start, edge_end)

    def add_vertex(self, new_vertex):
        return self.__graph.add_vertex(new_vertex)

    def add_edge(self, edge_start, edge_end, edge_cost):
        return self.__graph.add_edge(edge_start, edge_end, edge_cost)

    def remove_vertex(self, vertex_to_remove):
        return self.__graph.remove_vertex(vertex_to_remove)

    def remove_edge(self, edge_start, edge_end):
        return self.__graph.remove_edge(edge_start, edge_end)

    def read_activities_graph(self, file_path: str = "data/graph1k.txt") -> None:
        self.__graph = DirectedCostGraph()
        input_file = open(file_path, "rt")
        for file_format in input_file.readlines():
            file_format = file_format.strip('\n').split(' ')
            self.__graph.add_vertex(0)
            if len(file_format) == 3:
                current_vertex = file_format[0]
                cost = int(file_format[2])
                self.__graph.add_vertex(current_vertex)
                if file_format[1] != '-':
                    vertex_list = file_format[1].split(',')
                    for predecessor in vertex_list:
                        self.__graph.add_vertex(predecessor)
                        self.__graph.add_edge(predecessor, current_vertex, cost)
                elif file_format[1] == '-':
                    self.__graph.add_edge(0, current_vertex, cost)

        self.__graph_is_undirected = False
        input_file.close()
    def read_directed_graph(self, file_path: str = "data/graph1k.txt") -> None:
        """
        :param file_path: path of input file to be read
        :return: None, changes internal dict_in, dict_out, dict_costs with values from the input file
        having the convention format:
            line 0:    number_of_vertices number_of_edges
            line 1:    edge1_start edge1_end edge1_cost
            line 2:    edge2_start edge2_end edge2_cost
            ............................................
            line n:    edgeN_start edgeN_end edgeN_cost
        OR:
            line 0:    edge0_start edge0_end edge0_cost
            line 1:    isolated_node
            line 2:    edge2_start edge2_end edge2_cost
            ............................................
            line n:    edgeN_start edgeN_end edgeN_cost OR isolated_node
        E.g 1:                              E.g 2:
            5 6                             0 1 3
            0 0 1                           2
            0 1 7                           3 4 10
            1 2 2                           32
            2 1 -1                          4 7 13
            1 3 8
            2 3 5
        """
        self.__graph = DirectedCostGraph()
        input_file = open(file_path, "rt")
        file_format = input_file.readline().strip('\n').split(' ')
        if len(file_format) == 2:
            number_of_vertices = int(file_format[0])
            number_of_edges = int(file_format[1])
            self.__graph.initialize_vertices(number_of_vertices)
            for i in range(number_of_edges):
                correct_line = input_file.readline().strip('\n').split(' ')
                edge_start = int(correct_line[0])
                edge_end = int(correct_line[1])
                edge_cost = int(correct_line[2])
                self.__graph.add_edge(edge_start, edge_end, edge_cost)
        else:
            if len(file_format) == 1:
                self.__graph.add_vertex(int(file_format[0]))
            elif len(file_format) == 3:
                self.__graph.add_vertex(int(file_format[0]))
                self.__graph.add_vertex(int(file_format[1]))
                self.__graph.add_edge(int(file_format[0]), int(file_format[1]), int(file_format[2]))
            for current_line in input_file.readlines():
                correct_line = current_line.strip('\n').split(' ')
                if len(correct_line) == 1:
                    self.__graph.add_vertex(int(correct_line[0]))
                if len(correct_line) == 3:
                    edge_start = int(correct_line[0])
                    edge_end = int(correct_line[1])
                    edge_cost = int(correct_line[2])
                    self.__graph.add_vertex(edge_start)
                    self.__graph.add_vertex(edge_end)
                    self.__graph.add_edge(edge_start, edge_end, edge_cost)
        self.__graph_is_undirected = False
        input_file.close()

    def read_undirected_graph(self, file_path: str = "data/input.tx"):
        self.__graph = DirectedCostGraph()
        input_file = open(file_path, "rt")
        file_format = input_file.readline().strip('\n').split(' ')
        if len(file_format) == 2:
            number_of_vertices = int(file_format[0])
            number_of_edges = int(file_format[1])
            self.__graph.initialize_vertices(number_of_vertices)
            for i in range(number_of_edges):
                correct_line = input_file.readline().strip('\n').split(' ')
                edge_start = int(correct_line[0])
                edge_end = int(correct_line[1])
                edge_cost = int(correct_line[2])
                if edge_start == edge_end:
                    continue
                self.__graph.add_edge(edge_start, edge_end, edge_cost)
                self.__graph.add_edge(edge_end, edge_start, edge_cost)
        else:
            if len(file_format) == 1:
                self.__graph.add_vertex(int(file_format[0]))
            elif len(file_format) == 3:
                edge_start = int(file_format[0])
                edge_end = int(file_format[1])
                edge_cost = int(file_format[2])
                self.__graph.add_vertex(edge_start)
                if edge_start != edge_end:
                    self.__graph.add_vertex(edge_end)
                    self.__graph.add_edge(edge_start, edge_end, edge_cost)
                    self.__graph.add_edge(edge_end, edge_start, edge_cost)
            for current_line in input_file.readlines():
                correct_line = current_line.strip('\n').split(' ')
                if len(correct_line) == 1:
                    self.__graph.add_vertex(int(correct_line[0]))
                if len(correct_line) == 3:
                    edge_start = int(correct_line[0])
                    edge_end = int(correct_line[1])
                    edge_cost = int(correct_line[2])
                    self.__graph.add_vertex(edge_start)
                    if edge_start == edge_end:
                        continue
                    self.__graph.add_vertex(edge_end)
                    self.__graph.add_edge(edge_start, edge_end, edge_cost)
                    self.__graph.add_edge(edge_end, edge_start, edge_cost)
        self.__graph_is_undirected = True
        input_file.close()

    def write_graph_data(self, file_path: str = "data/input.txt"):
        """
        This function writes the graph into the file specified by file_path parameter in a certain format
        :parameter file_path: the path of the file to be written
        file format after write is:
            line 0 :            edge1_start edge1_end edge1_cost
            line 0 :            edge1 --------> isolated node
            line 0:    number_of_vertices number_of_edges
            line 1:    edge1_start edge1_end edge1_cost
            line 2:    edge2_start edge2_end edge2_cost
            ............................................
            line n:    edgeN_start edgeN_end edgeN_costs
        E.g:
            2 3
            1 1 1
            0 1 5
            1 0 3
        """
        output_file = open(file_path, "wt")
        for vertex in self.__graph.parse_all_vertices():
            # isolated node case
            if self.__graph.get_in_degree(vertex) == 0 and self.__graph.get_out_degree(vertex) == 0:
                output_file.write(f'{vertex}' + "\n")
                continue
            for edge in self.__graph.parse_out_edges(vertex):
                output_file.write(f'{edge[0]} {edge[1]} {self.get_edge_cost(edge[0], edge[1])}' + "\n")
        output_file.close()

    def random_directed_graph(self, number_of_vertices, number_of_edges, cost_range: tuple = (0, 99)) -> bool:
        """
        Replaces the current graph with a random graph with specified number of vertices and edges
        :param number_of_vertices: the number of vertices that the random graph will have
        :param number_of_edges: number of edges the random graph will have
        :param cost_range: a range of values that the edge costs may take
        :return False if the precondition that number of edges is less than number the number of vertices^2
                True if built successfully
        """
        if number_of_edges > number_of_vertices * number_of_vertices:
            return False
        random_graph = DirectedCostGraph()
        random_graph.initialize_vertices(number_of_vertices)
        cost_range_start = cost_range[0]
        cost_range_end = cost_range[1]
        i = 0
        while i < number_of_edges:
            edge_start = random.randint(0, number_of_vertices - 1)
            edge_end = random.randint(0, number_of_vertices - 1)
            cost = random.randint(cost_range_start, cost_range_end)
            if random_graph.add_edge(edge_start, edge_end, cost):
                i += 1
        self.__graph = random_graph
        self.__graph_is_undirected = False
        return True

    def random_undirected_graph(self, number_of_vertices, number_of_edges, cost_range: tuple = (0, 99)):
        pass

    def make_graph_copy(self):
        self.__last_copy = self.__graph.get_copy()
        if self.__last_copy != self.__graph:
            return True
        return False

    def revert_to_last_copy(self):
        if self.__last_copy == self.__graph:
            return False
        self.__graph = self.__last_copy
        return True

    def BFS(self, start: int):
        if not self.__graph.is_vertex(start):
            return None
        queue = []
        parent = {}
        queue.append(start)
        parent[start] = None
        while len(queue) != 0:
            current_vertex = queue.pop()
            for successor in self.__graph.parse_out_vertices(current_vertex):
                if successor not in parent:
                    parent[successor] = current_vertex
                    queue.append(successor)
        return parent

    def connected_components_BFS(self) -> list:
        """
                Goes through all the connected components of the current graph and creates the appropriate subgraphs
            representing each connected component. To achieve this, we use BFS on each node of the current graph,
            marking the nodes visited by BFS such that we don't check the same connected component twice.
        :return: a list of subgraphs representing the connected components of the current graph
        """
        # Remember visited vertices
        visited = {}
        # The list of subgraphs
        connected_components = []
        # Go through all vertices
        for vertex in self.__graph.parse_all_vertices():
            # Check if they are not in an already parsed connected component
            if vertex not in visited:
                # Do a BFS on the current vertex that is not in any of the previous connected components and remember all the vertices parsed by BFS
                parents = self.BFS(vertex)
                # Initiate current subgraph (connected component of the big graph)
                current_connected_component = DirectedCostGraph()
                # Go through all vertices parsed by BFS
                for accessible_vertex_in_component in parents:
                    # Add vertex parsed by BFS to subgraph
                    current_connected_component.add_vertex(accessible_vertex_in_component)
                    # Mark vertex as visited
                    visited[accessible_vertex_in_component] = True
                    # Parse all neighbours of the current vertex to add ALL edges of the current vertex
                    for neighbour in self.__graph.parse_out_vertices(accessible_vertex_in_component):
                        # Add edge to the subgraph
                        edge_cost = self.__graph.get_edge_cost(accessible_vertex_in_component, neighbour)
                        current_connected_component.add_vertex(neighbour)
                        current_connected_component.add_edge(accessible_vertex_in_component, neighbour, edge_cost)
                        current_connected_component.add_edge(neighbour, accessible_vertex_in_component, edge_cost)
                connected_components.append(current_connected_component)
        return connected_components

    @staticmethod
    def find_path_from_predecessors(predecessors: dict, final_vertex):
        """

        :param predecessors: a dict where the key-value pair means that the value is the predecessor vertex of the key.
                                so for the edge 1 --> 2, the correct predecessor dict would have predecessor[2] = 1
        :param final_vertex: the vertex where the path ends. We have its predecessor in predecessors dict and we can move
                                from predecessor to predecessor until we reach None (reaching the top node) to find the path
        :return: a list containing on index 0 the start vertex of the path and the vertices needed to reach the final_vertex
                    in consecutive order.
                    E.g: path: [3, 4, 2, 5, 0]
                    this means that to reach vertex 0 from 3 we have to go 3 --> 4 --> 2 --> 5 --> 0
        """
        # Initiate the path with the destination vertex
        path = [final_vertex]
        current = predecessors[final_vertex]
        # Parse the predecessors dict while constructing the path
        while current is not None:
            path.append(current)
            current = predecessors[current]
        # By going through the predecessors the path will be reversed, therefore we fix it through reversing it back
        path.reverse()
        return path

    def shortest_path(self, start_vertex, end_vertex):
        """
            Computes the shortest path from the start vertex to the end vertex using Bellman-Ford algorithm and returns
        the distance to that vertex (integer) and the correct path to the end vertex (a list of vertices)
        If there exists a negative cycle, then the algorithm returns false
        :param start_vertex: vertex to start path from
        :param end_vertex: vertex to end path to

        distance -> a dictionary that maps the distance from the start_vertex to the key of distance, so
                    distance[3] is the distance from start_vertex to vertex 3
        predecessor -> a dictionary that maps the key vertex to its parent vertex, so for an edge 1->2
                        predecessor[2] = 1

        :return: False if there exists a negative cycle from the start vertex
                Else
                returns distance, path --> distance is an integer representing the minimum cost to get from start_vertex to end_vertex
                                       --> path is a list representing the vertices needed to get from start_vertex to end_vertex
                                            by iterating ascending through the list we get the path starting from start_vertex to end_vertex
        """
        # Prerequisites
        distance = {}
        predecessor = {}
        """ Initialize the default values for all vertices in distance and predecessor """
        for vertex in self.__graph.parse_all_vertices():
            distance[vertex] = float('inf')
            predecessor[vertex] = None
        # Distance to from start to start is ofcourse 0
        distance[start_vertex] = 0

        """ Relax the graph at most N - 1 times (where N is the number of vertices of the current graph) or until we no longer get any changes
         We relax it N - 1 times because the longest possible path from start_vertex to end_vertex would include N - 1 edges """
        changed = True
        i = 0
        while changed and i < self.__graph.get_number_of_vertices():
            changed = False
            i += 1
            # Parse ALL edges of the graph
            for edge in self.__graph.parse_all_edges():
                edge_start = edge[0]
                edge_end = edge[1]
                cost = self.__graph.get_edge_cost(edge_start, edge_end)
                # Check if we found a better distance from start_vertex to the current vertex
                if distance[edge_start] + cost < distance[edge_end]:
                    changed = True
                    # Update the distance with the new-found better distance
                    distance[edge_end] = distance[edge_start] + cost
                    # Update the predecessor dict used to create the path
                    predecessor[edge_end] = edge_start

        """ Check for negative cycles """
        for vertex in self.__graph.parse_all_vertices():
            prev = predecessor[vertex]
            if prev is None:
                continue
            cost = self.__graph.get_edge_cost(prev, vertex)
            if distance[prev] + cost < distance[vertex]:
                # This means we found a negative cycle
                # Maybe raise exception instead of returning false, not sure
                return False

        """ Compute the path from the predecessors """
        path = self.find_path_from_predecessors(predecessor, end_vertex)
        return distance[end_vertex], path

    def topological_sort_counting_predecessors(self):
        if self.__graph.get_number_of_vertices() == 0:
            return None

        # Dict with the number of predecessors of each vertex
        in_degree = {}
        # The final sorted vertices
        result = []
        # deque for the nodes with no predecessors for parsing
        queue = deque()
        # Update for each vertex its number of predecessors in dict
        for vertex in self.__graph.parse_all_vertices():
            number_of_predecessors = self.__graph.get_in_degree(vertex)
            if number_of_predecessors == 0:
                queue.append(vertex)
            in_degree[vertex] = self.__graph.get_in_degree(vertex)

        # Process vertices with no predecessors
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            # Decrement incoming edges for each successor
            for successor in self.__graph.parse_out_vertices(vertex):
                in_degree[successor] -= 1
                if in_degree[successor] == 0:
                    queue.append(successor)

        # If all vertices have been added to the graph, then it is a DAG
        if len(result) == self.__graph.get_number_of_vertices():
            return result
        # Else, it has a cycle
        return None

    def earliest_start(self):
        sorted_vertices = self.topological_sort_counting_predecessors()
        if sorted_vertices is None:
            return None
        earliest_start_time = {}
        for vertex in sorted_vertices:
            max_time = 0
            for predecessor in self.__graph.parse_in_vertices(vertex):
                max_time = max(max_time, earliest_start_time[predecessor] + self.get_edge_cost(predecessor, vertex))
            earliest_start_time[vertex] = max_time
        max_total_time = 0
        for key in earliest_start_time:
            max_total_time = max(max_total_time, earliest_start_time[key])
        return earliest_start_time

    def latest_start(self):
        sorted_vertices = self.topological_sort_counting_predecessors()
        if sorted_vertices is None:
            return None
        latest_start_times = {}
        earliest_start_times = self.earliest_start()
        for vertex in self.__graph.parse_all_vertices():
            latest_start_times[vertex] = float('inf')
        # Nth vertex
        index = self.get_number_of_vertices() - 2
        latest_start_times[index + 1] = earliest_start_times[index + 1]
        # Parse in reverse topological order
        while index >= 0:
            min_time = float('inf')
            for successor in self.__graph.parse_out_vertices(sorted_vertices[index]):
                min_time = min(min_time, latest_start_times[successor] - self.get_edge_cost(sorted_vertices[index], successor))
            latest_start_times[sorted_vertices[index]] = min_time
            index -= 1
        return latest_start_times

    def critical_activities(self):
        earliest_times = self.earliest_start()
        if earliest_times is None:
            return None
        latest_times = self.latest_start()
        critical_vertices = []
        for vertex in self.__graph.parse_all_vertices():
            if earliest_times[vertex] == latest_times[vertex]:
                critical_vertices.append(vertex)
        return critical_vertices