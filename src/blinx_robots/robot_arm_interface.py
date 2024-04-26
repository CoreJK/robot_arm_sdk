import json

import numpy as np
from loguru import logger
from spatialmath import SE3
from spatialmath.base import rpy2tr

from .robot_arm_module import BlinxRobotArm


class BlxRobotArm(object):
    """比邻星六轴机械臂 API"""

    def __init__(self, communication_strategy):
        self.blinx_robot_arm = BlinxRobotArm()
        self.communication_strategy = communication_strategy

    def set_communication_strategy(self, communication_strategy):
        """设置机械臂的不同连接方式"""
        self.communication_strategy = communication_strategy
    
    def start_communication(self):
        """机械臂开始连接"""
        # todo 不同的连接策略，需要返回不同的连接对象
        self.client = self.communication_strategy.connect()
    
    def command_sender(self, command: str) -> dict:
        """发送命令到机械臂
        :param command: 机械臂命令
        """
        # todo 不同的连接策略，发送，接收命令的方式可能不同
        self.client.send(command.encode('utf-8'))
        data = json.loads(self.client.recv(1024).decode())
        return data
    
    def set_robot_arm_init(self) -> dict:
        """机械臂初始化，将机械臂关节角度归零
        :return: {"command": "set_joint_return_to_zero", "data": "true"}
        """
        payload = [0]
        command = json.dumps({"command": "set_joint_return_to_zero", "data": payload}).replace(' ', "").strip() + '\r\n'
        data = self.command_sender(command)
            
        return data

    def set_joint_degree_by_number(self, joint_number: int, speed_percentage: int, joint_degree: float) -> dict:
        """设置指定的机械臂关节角度
        :param joint_number: 机械臂关节编号 1~6
        :param speed_percentage: 机械臂关节运动速度百分比 1~100
        :param joint_degree: 机械臂关节角度, 单位:度
        """
        payload = [joint_number, speed_percentage, joint_degree]
        command = json.dumps({"command": "set_joint_angle", "data": payload}).replace(' ', "").strip() + '\r\n'
        data = self.command_sender(command)
            
        return data

    def set_joint_degree_synchronize(self, *args, speed_percentage: int = 50) -> dict:
        """设置机械臂所有关节角度
        :param *args: 机械臂所有关节的角度 q1, q2, q3, q4, q5, q6, 单位:度
        :param speed_percentage: 机械臂关节运动速度百分比 1~100
        """
        if len(args) == 6:
            joints_degree = list(args)
            payload = [speed_percentage]
            payload.extend(joints_degree)
            command = json.dumps({"command": "set_joint_angle_all_time", "data": payload}).replace(' ', "").strip() + '\r\n'
            data = self.command_sender(command)
            return data
        else:
            logger.error("关节超出范围!")
            return json.dumps({"command": "set_joint_angle_all_time", "status": "false"})

    def set_robot_io_interface(self, io: int, status: bool) -> dict:
        """设置机械臂 IO 口状态
        :param io: 机械臂IO口, 0~3
        :param status: 机械臂IO口状态, True:打开, False:关闭
        """
        command = json.dumps({"command": "set_robot_io_interface", "data": [io, status]}).replace(' ', "").strip() + '\r\n'
        data = self.command_sender(command)
        return data

    def set_joint_degree_by_coordinate(self, *args, speed_percentage: int) -> dict:
        """通过末端工具坐标与姿态，控制机械臂关节运动
        :param *args: 机械臂末端工具坐标与姿态: x, y, z, Rx, Py, Yz
        :param speed_percentage: 机械臂关节运动速度百分比 1~100
        """
        # 通过末端工具坐标与姿态，计算机械臂逆解
        inverse_solution = json.loads(self.get_inverse_solution(*args)).get('data')
        if inverse_solution:
            # 设置机械臂关节角度
            execute_result = self.set_joint_degree_synchronize(*inverse_solution, speed_percentage=50)
            return execute_result
        else:
            logger.error("获取机械臂逆解失败!")
            return json.dumps({"command": "set_coordinate_axle_all_speed", "status": "false"})

    def get_joint_degree_all(self) -> dict:
        """获取机械臂所有关节角度"""
        command = json.dumps({"command": "get_joint_angle_all"}).replace(' ', "").strip() + '\r\n'
        data = self.command_sender(command)
        return data

    def get_positive_solution(self, *args, current_pose=False) -> str:
        """获取机械臂正解
        根据提供的机械臂各个关节的角度，计算出机械臂末端的位置和姿态

        :params args: 机械臂关节角度值 q1, q2, q3, q4, q5, q6, 单位:度
        :params current_pose: 是否使用当前机械臂关节角度值, 默认为 False, False 可以不用提供所有关节角度值
        """
        if current_pose:
            joint_angle_list = self.get_joint_degree_all().get('data')
        else:
            joint_angle_list = list(args)

        if joint_angle_list and len(joint_angle_list) == 6:
            # 计算机械臂正解
            arm_joint_radians = np.radians(joint_angle_list)
            translation_vector = self.blinx_robot_arm.fkine(arm_joint_radians)
            x, y, z = np.round(translation_vector.t, 3)  # 平移向量
            Rx, Py, Yz = np.round(translation_vector.rpy(order="zyx"), 3)  # 旋转角
            positive_solution = json.dumps({"command": "get_positive_solution", "data": [x, y, z, Rx, Py, Yz]})
            return positive_solution
        else:
            logger.error("获取机械臂角度值失败!")
            positive_solution = json.dumps({"command": "get_positive_solution", "data": []})
            return positive_solution

    def get_inverse_solution(self, *args, current_pose=False) -> str:
        """获取机械臂逆解
        :params *args: 机械臂 x, y, z, Rx, Py, Yz 坐标
        :params current_pose: 是否使用当前机械臂关节角度值
        """
        if current_pose:
            positive_solution = json.loads(self.get_positive_solution(current_pose=True)).get('data')
            x, y, z, Rx, Py, Yz = positive_solution
        else:
            x, y, z, Rx, Py, Yz = list(args)

        R_T = SE3([x, y, z]) * rpy2tr([Rx, Py, Yz], order='zyx')
        sol = self.blinx_robot_arm.ikine_LM(R_T, joint_limits=True)
        if sol.success:
            inverse_result = np.round(np.degrees(sol.q), 3).tolist()
            return json.dumps({"command": "get_inverse_kinematics", "data": inverse_result})
        else:
            logger.error("获取机械臂逆解失败!")
            return json.dumps({"command": "get_inverse_kinematics", "data": []})
