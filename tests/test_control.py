# -*- coding: utf-8 -*-
# 测试 SDK 控制机械臂功能的代码
import time
from blinx_robots.robot_arm_interface import BlxRobotArm
from blinx_robots.robot_arm_communication import SocketCommunication


if __name__ == "__main__":
    
    # 连接机械臂
    host = "192.168.10.234"
    port = 1234
    socket_communication = SocketCommunication(host, port)
    robot = BlxRobotArm(socket_communication)
    robot.start_communication()
    
    # 机械臂初始化，将机械臂关节角度归零
    # print(robot.set_robot_arm_init())
    # time.sleep(12)
    
    # # 获取机械臂关节角度
    print(robot.get_joint_degree_all())
    time.sleep(1)
    
    # # 设置指定的机械臂关节角度
    # print(robot.set_joint_degree_by_number(1, 50, 50))
    
    # # 设置机械臂所有关节角度同时运动
    # print(robot.set_joint_degree_synchronize(0, 0, 0, 0, 0, 0, speed_percentage=50))
    
    # # 获取机械臂正解
    # print(robot.get_positive_solution(50, 0, 0, 0, 0, 0, current_pose=False))  # 传入自定义关节角度值获取正解
    # print(robot.get_positive_solution(current_pose=True))  # 根据机械臂当前关节角度获取正解
    
    # # 获取机械臂逆解
    # print(robot.get_inverse_solution(0.157, 0.187, 0.269, 0.0, -0.0, 0.873, current_pose=False))  # 传入自定义末端位姿获取逆解
    # print(robot.get_inverse_solution(current_pose=True))  # 根据机械臂当前末端位姿获取逆解
    
    # # 根据坐标系位置和姿态控制机械臂运动
    # print(robot.set_joint_degree_by_coordinate(0.157, 0.187, 0.269, 0.0, -0.0, 0.873, speed_percentage=50))
    
    # # 控制IO口
    # print(robot.set_robot_io_interface(0, True))  # 打开IO口
    # print(robot.set_robot_io_interface(0, False))  # 关闭IO口
    
    robot.client.close()
    