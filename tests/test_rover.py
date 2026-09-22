import unittest

from src.rover import Rover, run_scenario


class RoverTests(unittest.TestCase):
    def test_move_forward_north(self):
        rover = Rover(0, 0, "N")
        rover.move_forward()
        self.assertEqual(rover.state(), (0, 1, "N"))

    def test_turn_left_from_north(self):
        rover = Rover(0, 0, "N")
        rover.turn_left()
        self.assertEqual(rover.orientation, "W")

    def test_turn_right_from_north(self):
        rover = Rover(0, 0, "N")
        rover.turn_right()
        self.assertEqual(rover.orientation, "E")

    def test_obstacle_blocks_move(self):
        rover = Rover(0, 0, "N", obstacles={(0, 1)})
        rover.move_forward()
        self.assertEqual(rover.state(), (0, 0, "N"))

    def test_run_scenario_with_obstacle(self):
        scenario = "START 0 0 N\nOBSTACLE 0 2\nCOMMANDS FFRFF\n"
        self.assertEqual(run_scenario(scenario), (2, 1, "E"))


if __name__ == "__main__":
    unittest.main()
