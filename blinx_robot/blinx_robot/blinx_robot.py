from functools import wraps
import socket
import json
import time
from math import radians, degrees

from loguru import logger
import numpy as np
from retrying import retry

from blinx_robot_module import Mirobot


def limit_robot_arm_joint(max_args):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检查机械臂关节个数是否超过最大值
            if len(args) > max_args:
                raise ValueError("机械臂关节个数不能超过 {} 个".format(max_args))

            # 检查所有入参是否为数字
            check_args = all([isinstance(i, (int, float)) for i in args])
            if not check_args:
                raise ValueError("机械臂关节角度值必须为整数或浮点数")
            return func(*args, **kwargs)
        return wrapper
    return decorator


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
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.client = ClientSocket(self.host, self.port).new_connect()
        self.robot = Mirobot()

    def set_joint_auto_zero(self):
        """设置机械臂关节自动归零运动
        :return: {"command": "set_joint_Auto_zero", "data": "true"}
        """
        command = json.dumps({"command": "set_joint_Auto_zero"}).replace(' ', "").strip() + '\r\n'
        self.client.send(command.encode('utf-8'))
        data = json.loads(self.client.recv(1024).decode())
        return data

    def set_joint_angle(self, axle, angle):
        """设置指定的机械臂关节角度
        :param axle: 机械臂关节
        :param angle: 机械臂关节角度
        """
        command = json.dumps({"command": "set_joint_angle", "data": [axle, angle]}).replace(' ', "").strip() + '\r\n'
        self.client.send(command.encode('utf-8'))
        data = json.loads(self.client.recv(1024).decode())
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
        return data

    def set_joint_angle_all_speed(self, *args, speed=50):
        """设置指定的机械臂关节角度
        :param args: 机械臂关节角度值
        :param speed: 机械臂关节运动速度
        """
        six_angle = list(args)
        six_angle.append(speed)
        command = json.dumps({"command": "set_joint_angle_all_speed", "data": six_angle}).replace(' ', "").strip() + '\r\n'
        self.client.send(command.encode('utf-8'))
        data = json.loads(self.client.recv(1024).decode())
        return data

    def get_positive_solution(self, *args, current_pose=False):
        """获取机械臂正解
        :params args: 机械臂关节角度值
        :params current_pose: 是否使用当前机械臂关节角度值
        """
        if current_pose:
            joint_angle_list = self.get_joint_angle_all().get('data')
        else:
            joint_angle_list = list(*args)
            
        if joint_angle_list:
            # 提取机械臂角度值
            arm_pose_list = [round(float(data), 2) for data in joint_angle_list]
            arm_pose_degrees = np.array(arm_pose_list)
            # 计算机械臂正解
            translation_vector = self.robot.fkine(arm_pose_degrees)
            x, y, z = translation_vector.t  # 平移向量
            Rz, Ry, Rx = map(lambda x: degrees(x), translation_vector.rpy())  # 旋转角
            positive_solution = json.dumps({"command": "get_positive_solution", "data": [x, y, z, Rx, Ry, Rz]})
            return positive_solution
        else:
            logger.error("获取机械臂角度值失败!")
            positive_solution = json.dumps({"command": "get_positive_solution", "data": []})
            return positive_solution

    def get_inverse_solution(self):
        """获取机械臂逆解"""
        pass

    def set_robot_io_interface(self, io, status):
        """设置机械臂IO口状态
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
    

if __name__ == "__main__":
    blx_robot_arm = BlxRobotArm("192.168.10.234", 1234)
    # print(blx_robot_arm.set_joint_auto_zero())
    # time.sleep(20)
    # print(blx_robot_arm.set_joint_angle(1, 45))
    # time.sleep(2)
    # print(blx_robot_arm.set_joint_angle_speed(1, 90, 50))
    # time.sleep(2)
    # print(blx_robot_arm.set_joint_angle_all_speed(50,50,50,50,50,50, speed=50))
    # time.sleep(2)

    print(blx_robot_arm.get_positive_solution(45, 90, 45, 90, 45, 90, current_pose=True))
    
