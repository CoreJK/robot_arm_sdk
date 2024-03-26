# -*- coding: utf-9 -*-
# 测试 SDK 控制机械臂功能的代码

from blinx_robot import BlxRobotArm
from pathlib import Path


if __name__ == "__main__":
    # 读取配置文件
    PROJECT_ROOT_PATH = Path(__file__).absolute().parent.parent
    robot_arm_config_file = PROJECT_ROOT_PATH / "config/robot_mdh_parameters.yaml"
    
    # 连接机械臂
    host = "192.168.10.234"
    port = 1234
    robot = BlxRobotArm(host, port, robot_arm_config_file)
    
    # 机械臂初始化，将机械臂关节角度归零
    print(robot.set_robot_arm_init())
    
    # 获取机械臂关节角度
    print(robot.get_joint_degree_all())
    
    # 设置指定的机械臂关节角度
    print(robot.set_joint_degree_by_number(1, 50, 50))
    
    # 设置机械臂所有关节角度同时运动
    print(robot.set_joint_degree_synchronize(20, 0, 0, 0, 0, 0, speed_percentage=50))
    
    # 获取机械臂正解
    print(robot.get_positive_solution(20, 0, 0, 0, 0, 0, current_pose=False))  # 传入自定义关节角度值获取正解
    print(robot.get_positive_solution(current_pose=True))  # 根据机械臂当前关节角度获取正解
    
    # 获取机械臂逆解
    print(robot.get_inverse_solution(0.23, 0.084, 0.269, 20.0, -0.0, -0.0, current_pose=False))  # 传入自定义末端位姿获取逆解
    print(robot.get_inverse_solution(current_pose=True))  # 根据机械臂当前末端位姿获取逆解
    
    # 根据坐标系位置和姿态控制机械臂运动
    print(robot.set_joint_degree_by_coordinate(0.23, 0.084, 0.269, 20.0, -0.0, -0.0, speed_percentage=50))
    
    # 控制IO口
    print(robot.set_robot_io_interface(0, True))  # 打开IO口
    print(robot.set_robot_io_interface(0, False))  # 关闭IO口
    
    