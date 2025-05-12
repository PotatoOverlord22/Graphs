from ui.console_ui import ConsoleUI
from domain.graph import DirectedCostGraph
from controller.graph_controller import GraphController

class App:
    @staticmethod
    def start():
        graph = DirectedCostGraph()
        controller = GraphController(graph)
        ui = ConsoleUI(controller)
        ui.start()


if __name__ == "__main__":
    app = App()
    app.start()
