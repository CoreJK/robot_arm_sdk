# -*- coding: utf-8 -*-
# 测试 SDK 控制机械臂功能的代码
import time
import json

from loguru import logger

from blinx_robots.robot_arm_interface import BlxRobotArm
from blinx_robots.robot_arm_communication import SocketCommunication


if __name__ == "__main__":
    try:
        # 连接机械臂
        host = "192.168.10.111"
        port = 1234
        socket_communication = SocketCommunication(host, port)
        robot = BlxRobotArm(socket_communication)
        
        # 机械臂通讯连接
        robot.start_communication()
        
        # 获取机械臂的命令执行模式
        robot_cmd_model = json.loads(robot.get_robot_cmd_model()).get('data') 
        logger.info(f"机械臂的命令执行模式: {robot_cmd_model}")
        
        # 设置机械臂的命令模式
        # robot.set_robot_cmd_mode("INT")
        # time.sleep(1)
        robot.set_robot_cmd_mode("SEQ")
        time.sleep(1)
        
        # 机械臂初始化，将机械臂关节角度归零
        robot.set_robot_arm_init()
        time.sleep(12)
        
        # 获取机械臂关节角度
        robot.get_joint_degree_all()
        
        # 设置机械臂单个关节角度
        robot.set_joint_degree_by_number(1, 50, 90)
        
        # 获取机械臂所有当前关节角度
        joint_degree = robot.get_joint_degree_all().get('data')
        logger.info(f"机械臂所有关节角度: {joint_degree}")
        time.sleep(1.5)
        
        # 机械臂紧急停止
        robot.set_robot_arm_emergency_stop()
        time.sleep(2)
        
        # 恢复机械臂状态
        robot.set_robot_arm_init()
        time.sleep(1)
        robot.set_robot_arm_init()
        time.sleep(12)
        
        # 设置机械臂末端工具控制
        robot.set_robot_end_tool(1, True)  # 控制气泵打开
        time.sleep(2)
        robot.set_robot_end_tool(1, False)  # 控制气泵关闭
        time.sleep(2)
        
        # 设置机械臂所有关节角度协同运动
        robot.set_joint_degree_synchronize(10, 10, 10, 10, 10, 10, speed_percentage=50)
        time.sleep(2)
        
        # 通过末端工具坐标与姿态，控制机械臂关节运动
        robot.set_joint_degree_by_coordinate(0.287, 0.0, 0.269, 0.0, -0.0, 0.0, speed_percentage=50)
        time.sleep(5)
        
        # 机械臂回零
        robot.set_robot_arm_home()
        time.sleep(2)
        
        # 获取机械臂正解
        robot.get_positive_solution(current_pose=True)
        robot.get_positive_solution(20, 0, 0, 0, 0, 0, current_pose=False)
        
        # 获取机械臂逆解
        robot.get_inverse_solution(current_pose=True)
        robot.get_inverse_solution(0.23, 0.084, 0.269, 20.0, -0.0, -0.0, current_pose=False)
        
        # 机械臂通讯关闭
        robot.end_communication()
        
    # 用户输入  crt + c 退出
    except KeyboardInterrupt:        
        robot.end_communication()
    
