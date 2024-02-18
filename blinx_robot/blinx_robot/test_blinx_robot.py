import unittest
from blinx_robot import BlxRobotArm


class TestBlxRobotArm(unittest.TestCase):
    def setUp(self):
        self.robot = BlxRobotArm("192.168.10.235", 1234)

    def test_set_joint_auto_zero(self):
        result = self.robot.set_joint_auto_zero()
        self.assertEqual(result, {'return': 'set_joint_Auto_zero', 'data': 'true'})

    def test_set_joint_angle(self):
        result = self.robot.set_joint_angle(1, 45)
        self.assertEqual(result, {'data': 'true', 'return': 'set_joint_angle'})

    def test_set_joint_angle_speed(self):
        result = self.robot.set_joint_angle_speed(2, 30, speed=50)
        self.assertEqual(result, {'data': 'true', 'return': 'set_joint_angle_speed'})

    def test_set_joint_angle_all_speed(self):
        result = self.robot.set_joint_angle_all_speed(20, 20, 20, 20, 20, 20, speed=30)
        self.assertEqual(result, {'data': 'true', 'return': 'set_joint_angle_all_speed'})

    # def test_get_positive_solution(self):
    #     result = self.robot.get_positive_solution(20, 20, 20, 20, 20, 20, current_pose=False)
    #     self.assertEqual(result, {"command": "get_positive_solution", "data": [1.0, 2.0, 3.0, 10.0, 20.0, 30.0]})

    # def test_get_inverse_solution(self):
    #     result = self.robot.get_inverse_solution(1.0, 2.0, 3.0, 10.0, 20.0, 30.0)
    #     self.assertEqual(result, {"command": "get_inverse_kinematics", "data": [0, 30, 60, 90, 120, 150]})

    # def test_set_robot_io_interface(self):
    #     result = self.robot.set_robot_io_interface(1, "on")
    #     self.assertEqual(result, {"command": "set_robot_io_interface", "data": [1, "on"]})

    # def test_get_joint_angle_all(self):
    #     result = self.robot.get_joint_angle_all()
    #     self.assertEqual(result, {"command": "get_joint_angle_all"})

    # def test_set_coordinate_axle_all_speed(self):
    #     result = self.robot.set_coordinate_axle_all_speed(1.0, 2.0, 3.0, 10.0, 20.0, 30.0, speed=50)
    #     self.assertEqual(result, {"command": "set_joint_angle_all_speed", "data": [0, 30, 60, 90, 120, 150, 50]})

    
if __name__ == '__main__':
    unittest.main()