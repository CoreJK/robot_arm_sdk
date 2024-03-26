import socket
import json

from loguru import logger
import numpy as np
from retrying import retry
from spatialmath import SE3
from spatialmath.base import rpy2tr

from blinx_robot_module import Mirobot


# 机械臂连接方式
class ClientSocket:
    """客户端套接字"""
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @retry(stop_max_attempt_number=3, wait_fixed=1000)
    def new_connect(self):
        try:
            logger.info("正在尝试连接机械臂...")
            self.client.connect((self.host, self.port))
            logger.info("连接成功!")
        except Exception as e:
            logger.error("连接失败!失败原因：{}".format(e))
        return self.client
    

class BlxRobotArm(object):
    """比邻星六轴机械臂 API"""
    def __init__(self, host, port, config_file):
        self.host = host
        self.port = port
        self.config_file = config_file
        self.client = ClientSocket(self.host, self.port).new_connect()
        self.robot = Mirobot(self.config_file)

    def set_joint_auto_zero(self):
        """设置机械臂关节自动归零运动
        :return: {"command": "set_joint_Auto_zero", "data": "true"}
        """
        command = json.dumps({"command": "set_joint_return_to_zero", "data": [0]}).replace(' ', "").strip() + '\r\n'
        self.client.send(command.encode('utf-8'))
        data = json.loads(self.client.recv(1024).decode())
        self.client.close()
        return data

    def set_joint_angle(self, axle, angle):
        """设置指定的机械臂关节角度
        :param axle: 机械臂关节
        :param angle: 机械臂关节角度
        """
        command = json.dumps({"command": "set_joint_angle", "data": [axle, angle]}).replace(' ', "").strip() + '\r\n'
        self.client.send(command.encode('utf-8'))
        data = json.loads(self.client.recv(1024).decode())
        self.client.close()
        return data
    
    def set_joint_angle_speed(self, axle, angle, speed=50):
        """设置指定的机械臂关节角度
        :param axle: 机械臂关节
        :param angle: 机械臂关节角度
        :param speed: 机械臂关节运动速度
        """
        command = json.dumps({"command": "set_joint_angle_speed", "data": [axle, angle, speed]}).replace(' ', "").strip() + '\r\n'
        self.client.send(command.encode('utf-8'))
        data = json.loads(self.client.recv(1024).decode())
        self.client.close()
        return data

    def set_joint_angle_all_speed(self, *args, speed=50):
        """设置指定的机械臂关节角度
        :param args: 机械臂关节角度值
        :param speed: 机械臂关节运动速度
        """
        six_angle = list(args)
        if len(six_angle) != 6:
            logger.error("机械臂关节角度值必须为 6 个! 当前只传入了 {} 个".format(len(six_angle)))
            return json.dumps({"command": "set_joint_angle_all_speed", "data": []})
        
        six_angle.append(speed)
        command = json.dumps({"command": "set_joint_angle_all_speed", "data": six_angle}).replace(' ', "").strip() + '\r\n'
        self.client.send(command.encode('utf-8'))
        data = json.loads(self.client.recv(1024).decode())
        self.client.close()
        return data

    def get_positive_solution(self, *args, current_pose=False):
        """获取机械臂正解
        :params args: 机械臂关节角度值
        :params current_pose: 是否使用当前机械臂关节角度值
        """
        if current_pose:
            joint_angle_list = self.get_joint_angle_all().get('data')
        else:
            joint_angle_list = list(args)
            
        if joint_angle_list and len(joint_angle_list) == 6:
            # 计算机械臂正解
            arm_joint_radians = np.radians(joint_angle_list)
            translation_vector = self.robot.fkine(arm_joint_radians)
            x, y, z = np.round(translation_vector.t, 3)  # 平移向量
            Rx, Ry, Rz = np.round(translation_vector.rpy(unit="deg", order="xyz"), 3)  # 旋转角
            positive_solution = json.dumps({"command": "get_positive_solution", "data": [x, y, z, Rx, Ry, Rz]})
            self.client.close()
            return positive_solution
        else:
            logger.error("获取机械臂角度值失败!")
            positive_solution = json.dumps({"command": "get_positive_solution", "data": []})
            self.client.close()
            return positive_solution

    def get_inverse_solution(self, *args, current_pose=False):
        """获取机械臂逆解
        :params *args: 机械臂 x, y, z, Rx, Ry, Rz 坐标
        :params current_pose: 是否使用当前机械臂关节角度值
        """
        if current_pose:
            positive_solution = json.loads(self.get_positive_solution(current_pose=True)).get('data')
            x, y, z, Rx, Ry, Rz = positive_solution
        else:
            x, y, z, Rx, Ry, Rz = list(args)
        
        R_T = SE3([x, y, z]) * rpy2tr([Rz, Ry, Rx], unit='deg')
        sol = self.robot.ikine_LM(R_T, joint_limits=True)
        inverse_result = np.round(np.degrees(sol.q), 1).tolist()
        
        try:
            if len(inverse_result) == 6:
                return json.dumps({"command": "get_inverse_kinematics", "data": inverse_result})
            else:
                logger.error("获取机械臂逆解失败!")
                return json.dumps({"command": "get_inverse_kinematics", "data": []})
        except Exception as e:
            logger.error("获取机械臂逆解失败!失败原因：{}".format(e))
            return json.dumps({"command": "get_inverse_kinematics", "data": []})

    def set_robot_io_interface(self, io, status):
        """设置机械臂 IO 口状态
        :param io: 机械臂IO口
        :param status: 机械臂IO口状态
        """
        command = json.dumps({"command": "set_robot_io_interface", "data": [io, status]}).replace(' ', "").strip() + '\r\n'
        self.client.send(command.encode('utf-8'))
        data = json.loads(self.client.recv(1024).decode())
        return data

    def get_joint_angle_all(self):
        """获取机械臂所有关节角度"""
        command = json.dumps({"command": "get_joint_angle_all"}).replace(' ', "").strip() + '\r\n'
        self.client.send(command.encode('utf-8'))
        data = json.loads(self.client.recv(1024).decode())
        return data
    
    def set_coordinate_axle_all_speed(self, *args, speed):
        """通过末端工具坐标与姿态，控制机械臂关节运动"""
        # 通过末端工具坐标与姿态，计算机械臂逆解
        inverse_solution = json.loads(self.get_inverse_solution(*args)).get('data')
        if inverse_solution:
            # 设置机械臂关节角度
            execute_result = self.set_joint_angle_all_speed(*inverse_solution, speed=speed)
            return execute_result
            
    
