from model.simulation_model import SimulationModel
from view.simulation_view import SimulationView


class SimulationController:
    def __init__(self):
        self.view = SimulationView()

    def run_simulation(self):
        num_cubes = self.view.get_num_cubes()
        self.model = SimulationModel(num_cubes)
        opened_cubes, dead_students, days_survived = self.model.run()
        self.view.show_results(opened_cubes, dead_students, days_survived)
