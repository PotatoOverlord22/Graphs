from controller.graph_controller import GraphController
from errors.exceptions import GraphError, VertexNotIntegerError, EdgeInputError


class ConsoleUI:
    def __init__(self, graph_controller: GraphController):
        self.EXIT = '0'
        self.__graph_controller = graph_controller

    def start(self):
        while True:
            self.print_menu()
            user_option = self.read_general_user_input()
            if user_option == self.EXIT:
                return
            self.interpret_user_option(user_option)

    @staticmethod
    def read_general_user_input():
        return input("> ")

    @staticmethod
    def read_user_input_vertex():
        user_raw_vertex = input("vertex: ")
        try:
            user_vertex = int(user_raw_vertex)
        except ValueError:
            raise VertexNotIntegerError("Vertex is not an integer.")
        return user_vertex

    def read_user_input_edge(self):
        print("edge start: ")
        try:
            edge_start = self.read_user_input_vertex()
            print("edge end: ")
            edge_end = self.read_user_input_vertex()
        except VertexNotIntegerError as VertexError:
            raise EdgeInputError(VertexError)
        return edge_start, edge_end

    @staticmethod
    def print_menu():
        print("\nMenu:")
        print("\t1. Read directed graph from file")
        print("\t2. Read undirected graph from file")
        print("\t3. Write the current graph to a file")
        print("\t4. Make a copy of the graph")
        print("\t5. Get number of vertices")
        print("\t6. Get number of edges")
        print("\t7. Show all vertices")
        print("\t8. Check if edge")
        print("\t9. In degree and out degree of a vertex")
        print("\t10. Show outbound and inbound edges of a vertex")
        print("\t11. Get cost of an edge")
        print("\t12. Modify cost of an edge")
        print("\t13. Add vertex")
        print("\t14. Remove vertex")
        print("\t15. Add edge")
        print("\t16. Remove edge")
        print("\t17. Replace current graph with a random graph")
        print("\t18. Revert graph to last copy")
        print("\t19. Show the connected components of an UNDIRECTED graph")
        print("\t20. Show the minimum cost path between 2 given vertices")
        print("\t21. Write the lowest cost walks from between 2 given vertices in graph 1k,10k,100k.")
        print("\t22. Check if DAG")
        print("\t23. Earliest start")
        print("\t24. Latest start")
        print("\t25. Critical path")
        print("\t26. Read activities")
        print("\t0. EXIT")

    def interpret_user_option(self, user_option):
        GET_VERTICES = '5'
        GET_EDGES = '6'
        SHOW_VERTICES = '7'
        CHECK_IF_EDGE = '8'
        IN_OUT_DEGREE = '9'
        IN_OUT_EDGES = '10'
        GET_COST = '11'
        MODIFY_COST = '12'
        ADD_VERTEX = '13'
        REMOVE_VERTEX = '14'
        ADD_EDGE = '15'
        REMOVE_EDGE = '16'
        RANDOM_GRAPH = '17'
        READ_GRAPH = '1'
        READ_UNDIRECTED_GRAPH = '2'
        WRITE_GRAPH = '3'
        COPY_GRAPH = '4'
        REVERT_TO_LAST_COPY = '18'
        CONNECTED_COMPONENTS_BFS = '19'
        SHORTEST_PATH_FORD = '20'
        LOWEST_COST_WALKS_BIG_GRAPHS = '21'
        TOPOLOGICAL_SORT = '22'
        EARLIEST_START = '23'
        LATEST_START = '24'
        CRITICAL_PATH = '25'
        READ_ACTIVITIES = '26'

        if user_option == GET_VERTICES:
            print(f'The number of vertices is: {self.__graph_controller.get_number_of_vertices()}')
        elif user_option == GET_EDGES:
            print(f'The number of edges is: {self.__graph_controller.get_number_of_edges()}')
        elif user_option == SHOW_VERTICES:
            for vertex in self.__graph_controller.get_all_vertices():
                print(vertex, end=" ")
        elif user_option == CHECK_IF_EDGE:
            try:
                edge = self.read_user_input_edge()
            except EdgeInputError as EdgeError:
                print(EdgeError)
                return
            edge_start = edge[0]
            edge_end = edge[1]
            if self.__graph_controller.check_if_edge(edge_start, edge_end):
                print(f'Edge: ({edge_start}, {edge_end}) exists in the graph.')
            else:
                print(f'The edge does not exist.')
        elif user_option == IN_OUT_DEGREE:
            try:
                vertex_to_check = self.read_user_input_vertex()
                in_degree = self.__graph_controller.get_in_degree(vertex_to_check)
                out_degree = self.__graph_controller.get_out_degree(vertex_to_check)
            except VertexNotIntegerError as VE:
                print(VE)
                return
            except GraphError as GE:
                print(GE)
                return
            print(
                f'the IN degree of vertex {vertex_to_check} is: {in_degree}')
            print(
                f'the OUT degree of vertex {vertex_to_check} is: {out_degree}')
        elif user_option == IN_OUT_EDGES:
            try:
                vertex = self.read_user_input_vertex()
                outbound_edges = self.__graph_controller.get_outbound_edges(vertex)
                inbound_edges = self.__graph_controller.get_inbound_edges(vertex)
            except VertexNotIntegerError as VertexError:
                print(VertexError)
                return
            except GraphError as GE:
                print(GE)
                return
            print(f'The outbound edges of {vertex} are: ')
            for edge_tuple in outbound_edges:
                print(f'{edge_tuple[0]}-->{edge_tuple[1]}', end="  ")
            print(f'\nThe inbound edges of {vertex} are: ')
            for edge_tuple in inbound_edges:
                print(f'{edge_tuple[1]}<--{edge_tuple[0]}', end="  ")
        elif user_option == GET_COST:
            try:
                edge = self.read_user_input_edge()
                print(f'The cost of the edge {edge} is {self.__graph_controller.get_edge_cost(edge[0], edge[1])}')
            except EdgeInputError as EdgeError:
                print(EdgeError)
                return
            except GraphError as GE:
                print(GE)
                return

        elif user_option == MODIFY_COST:
            try:
                edge = self.read_user_input_edge()
                print("new cost: ")
                new_cost = int(self.read_general_user_input())
            except EdgeInputError as EdgeError:
                print(EdgeError)
                return
            except ValueError:
                print("Cost must be an integer.")
                return
            edge_start = edge[0]
            edge_end = edge[1]
            try:
                old_cost = self.__graph_controller.get_edge_cost(edge_start, edge_end)
                self.__graph_controller.modify_cost(edge_start, edge_end, new_cost)
            except GraphError as GE:
                print(GE)
                return
            print(f'Cost of edge ({edge_start}, {edge_end}) was modified from {old_cost} to {new_cost}')
        elif user_option == ADD_VERTEX:
            try:
                new_vertex = self.read_user_input_vertex()
            except VertexNotIntegerError as VertexError:
                print(VertexError)
                return
            if self.__graph_controller.add_vertex(new_vertex):
                print("Vertex added successfully.")
            else:
                print("Vertex already in graph.")
        elif user_option == REMOVE_VERTEX:
            try:
                vertex_to_remove = self.read_user_input_vertex()
            except VertexNotIntegerError as VertexError:
                print(VertexError)
                return
            if self.__graph_controller.remove_vertex(vertex_to_remove):
                print(f"Vertex {vertex_to_remove} was successfully removed.")
            else:
                print(f'Could not remove vertex {vertex_to_remove}.')
        elif user_option == ADD_EDGE:
            try:
                edge = self.read_user_input_edge()
                print("cost of edge: ")
                cost = int(self.read_general_user_input())
            except EdgeInputError as EdgeError:
                print(EdgeError)
                return
            except ValueError:
                print("Cost must be an integer.")
                return
            edge_start = edge[0]
            edge_end = edge[1]
            try:
                if self.__graph_controller.add_edge(edge_start, edge_end, cost):
                    print("Edge added successfully.")
                else:
                    print(f'Edge {edge} already exists.')
            except GraphError as GE:
                print(GE)
                return
        elif user_option == REMOVE_EDGE:
            try:
                edge = self.read_user_input_edge()
            except EdgeInputError as EdgeError:
                print(EdgeError)
                return
            edge_start = edge[0]
            edge_end = edge[1]
            if self.__graph_controller.remove_edge(edge_start, edge_end):
                print(f'Edge {edge} removed successfully.')
            else:
                print(f'Edge {edge} could not be removed.')
        elif user_option == RANDOM_GRAPH:
            try:
                print("number of vertices: ")
                number_of_vertices = int(self.read_general_user_input())
                print("number of edges: ")
                number_of_edges = int(self.read_general_user_input())
                self.__graph_controller.random_directed_graph(number_of_vertices, number_of_edges)
            except ValueError:
                print("Number of vertices and edges must be a number")
            except GraphError as GE:
                print(GE)
                return
            print("Graph successfully randomized.")
        elif user_option == READ_GRAPH:
            print("File location from parent folder(default for default location): ")
            file_path = self.read_general_user_input()
            if file_path == 'default':
                file_path = "data/input.txt"
            try:
                self.__graph_controller.read_directed_graph(file_path)
            except Exception:
                print("Reading graph from file was unsuccessful.")
                return
            print(f'Loaded graph from {file_path} successfully.')
        elif user_option == WRITE_GRAPH:
            print("File location from parent folder(default for default location): ")
            file_path = self.read_general_user_input()
            if file_path == 'default':
                file_path = "data/output.txt"
            if file_path.lower() == "default":
                file_path = "data/input.txt"
            self.__graph_controller.write_graph_data(file_path)
            print(f'Graph written successfully to {file_path}')
        elif user_option == COPY_GRAPH:
            if self.__graph_controller.make_graph_copy():
                print("Successfully copied graph.")
        elif user_option == REVERT_TO_LAST_COPY:
            if self.__graph_controller.revert_to_last_copy():
                print("Successfully reverted graph to last copy.")
                return
            print("Could not revert graph.")
        elif user_option == CONNECTED_COMPONENTS_BFS:
            list_of_connected_components = self.__graph_controller.connected_components_BFS()
            for i in range(len(list_of_connected_components)):
                print(f'Connected component {i + 1}: {list_of_connected_components[i].parse_all_vertices()}')
                for vertex in list_of_connected_components[i].parse_all_vertices():
                    print(list_of_connected_components[i].parse_out_edges(vertex))
        elif user_option == READ_UNDIRECTED_GRAPH:
            print("File location from parent folder(default for default location): ")
            file_path = self.read_general_user_input()
            if file_path == 'default':
                file_path = "data/input.txt"
            try:
                self.__graph_controller.read_undirected_graph(file_path)
            except Exception:
                print("Reading graph from file was unsuccessful.")
                return
            print(f'Loaded graph from {file_path} successfully.')
        elif user_option == SHORTEST_PATH_FORD:
            try:
                start_vertex = int(input("Start vertex: "))
                if start_vertex not in self.__graph_controller.get_all_vertices():
                    print("Vertex not in graph")
                    return
                end_vertex = int(input("End vertex: "))
                if end_vertex not in self.__graph_controller.get_all_vertices():
                    print("Vertex not in graph")
                    return
            except ValueError:
                print("Invalid vertex.")
                return
            returned = self.__graph_controller.shortest_path(start_vertex, end_vertex)
            if not returned:
                print("There exists a negative cycle!")
                return
            distance, path = returned
            if len(path) == 1:
                print(f'There is no path from {start_vertex} to {end_vertex}')
            else:
                print(f'Distance: {distance}')
                print(f'Path: {path}')
        elif user_option == LOWEST_COST_WALKS_BIG_GRAPHS:
            start_vertex = int(input("Start vertex: "))
            end_vertex = int(input("End vertex: "))
            write_file = open("data/lowest-cost-walks.txt", "wt")

            # Graph 1k
            self.__graph_controller.read_directed_graph("data/graph1k.txt")
            distance, path = self.__graph_controller.shortest_path(start_vertex, end_vertex)
            write_file.write(f'Graph1k {start_vertex} to {end_vertex}: distance: {distance},  path:{path}')
            distance, path = self.__graph_controller.shortest_path(end_vertex, start_vertex)
            write_file.write(f'\nGraph1k {end_vertex} to {start_vertex}: distance: {distance}, path: {path}')

            # Graph 10k
            self.__graph_controller.read_directed_graph("data/graph10k.txt")
            distance, path = self.__graph_controller.shortest_path(start_vertex, end_vertex)
            write_file.write(f'\nGraph10k {start_vertex} to {end_vertex}: distance: {distance},  path:{path}')
            distance, path = self.__graph_controller.shortest_path(end_vertex, start_vertex)
            write_file.write(f'\nGraph10k {end_vertex} to {start_vertex}: distance: {distance}, path: {path}')

            # Graph 100k
            self.__graph_controller.read_directed_graph("data/graph100k.txt")
            distance, path = self.__graph_controller.shortest_path(start_vertex, end_vertex)
            write_file.write(f'\nGraph100k {start_vertex} to {end_vertex}: distance: {distance},  path:{path}')
            distance, path = self.__graph_controller.shortest_path(end_vertex, start_vertex)
            write_file.write(f'\nGraph100k {end_vertex} to {start_vertex}: distance: {distance}, path: {path}')

            print("Done!")
            write_file.close()
        elif user_option == TOPOLOGICAL_SORT:
            sorted_graph = self.__graph_controller.topological_sort_counting_predecessors()
            if sorted_graph is None:
                print("Graph contains a cycle")
                return
            print(sorted_graph)
        elif user_option == EARLIEST_START:
            earliest_start = self.__graph_controller.earliest_start()
            if earliest_start is None:
                print("The graph could not be sorted")
                return
            print(earliest_start)
        elif user_option == LATEST_START:
            earliest_start = self.__graph_controller.latest_start()
            if earliest_start is None:
                print("The graph could not be sorted")
                return
            print(earliest_start)
        elif user_option == CRITICAL_PATH:
            critical_path = self.__graph_controller.critical_activities()
            if critical_path is None:
                print("The graph could not be topologically sorted")
                return
            print(critical_path)
        elif user_option == READ_ACTIVITIES:
            print("File location from parent folder(default for default location): ")
            file_path = self.read_general_user_input()
            if file_path == 'default':
                file_path = "data/input.txt"
            try:
                self.__graph_controller.read_activities_graph(file_path)
            except Exception:
                print("Reading graph from file was unsuccessful.")
                return
            print(f'Loaded graph from {file_path} successfully.')
        else:
            print("Unknown command.")
