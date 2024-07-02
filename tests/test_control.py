# -*- coding: utf-8 -*-
# 测试 SDK 控制机械臂功能的代码
import time
import json
import logging

from blinx_robots.robot_arm_interface import BlxRobotArm
from blinx_robots.robot_arm_communication import SocketCommunication

logging.disable(logging.CRITICAL)

if __name__ == "__main__":
    try:
        while True:
            # 连接机械臂
            host = "192.168.10.78"
            port = 1234
            socket_communication = SocketCommunication(host, port)
            robot = BlxRobotArm(socket_communication)
            
            # 机械臂通讯连接
            print("\n1: 测试机械臂通讯连接")
            robot.start_communication()
            
            # 获取机械臂的命令执行模式
            print("\n2: 测试机械臂命令执行模式")
            robot_cmd_model = json.loads(robot.get_robot_cmd_mode()).get('data') 
            print(f"机械臂的命令执行模式: {robot_cmd_model}")
            
            # 设置机械臂的命令模式
            print("\n3: 测试机械臂命令执行模式设置")
            robot.set_robot_cmd_mode("INT")
            time.sleep(1)
            print(robot.set_robot_cmd_mode("SEQ"))
            time.sleep(1)
            
            # 机械臂初始化，将机械臂关节角度归零
            print("\n4: 测试机械臂初始化")
            print(robot.set_robot_arm_init())
            time.sleep(12)
            
            # 获取机械臂关节角度
            print("\n5: 测试机械臂关节角度")
            print(robot.get_joint_degree_all())
            time.sleep(1)
            
            # 设置机械臂单个关节角度
            print("\n6: 测试机械臂单个关节角度设置")
            print(robot.set_joint_degree_by_number(1, 50, 90))
            
            # 获取机械臂所有当前关节角度
            print("\n7: 测试机械臂所有关节角度设置")
            joint_degree = robot.get_joint_degree_all().get('data')
            print(f"机械臂所有关节角度: {joint_degree}")
            time.sleep(1)
            
            # 机械臂紧急停止
            print("\n8: 测试机械臂紧急停止")
            print(robot.set_robot_arm_emergency_stop())
            time.sleep(2)
            
            # 恢复机械臂状态
            print("\n9: 测试机械臂急停后的状态恢复上电")
            print(robot.set_robot_arm_init())
            time.sleep(2)
            
            print("\n10: 测试机械臂急停后的状态恢复")
            print(robot.set_robot_arm_init())
            time.sleep(12)
            
            # 设置机械臂末端工具控制
            print("\n11: 测试机械臂末端工具控制使能")
            print(robot.set_robot_end_tool(1, True))  # 控制气泵打开
            time.sleep(2)
            print("\n12: 测试机械臂末端工具控制掉使能")
            print(robot.set_robot_end_tool(1, False))  # 控制气泵关闭
            time.sleep(2)
            
            # 设置机械臂末端 IO 控制
            print("\n13: 测试机械臂末端 IO 控制")
            print("\n1 号控制口打开")
            print(robot.set_robot_io_status(1, True))
            time.sleep(2)
            print("\n1 号控制口关闭")
            print(robot.set_robot_io_status(1, False))
            time.sleep(2)
            
            # 设置机械臂所有关节角度协同运动
            print("\n13: 测试机械臂所有关节角度协同运动")
            print(robot.set_joint_degree_synchronize(10, 10, 10, 10, 10, 10, speed_percentage=50))
            time.sleep(2)
            
            # 通过末端工具坐标与姿态，控制机械臂关节运动
            print("\n14: 测试通过末端工具坐标与姿态，控制机械臂关节运动")
            print(robot.set_robot_arm_coordinate(278.731, 0.000, 268.219, 180.000, -0.006, 0.000, speed_percentage=100))
            time.sleep(3)
            
            # 机械臂回零
            print("\n15: 测试机械臂回零")
            print(robot.set_robot_arm_home())
            time.sleep(2)
            
            # 获取机械臂正解
            print("\n16: 测试获取机械臂当前角度的正解值")
            print(robot.get_robot_coordinate())
            time.sleep(2)
            
            # 顺序执行模式中, 使用延时命令
            if robot_cmd_model == "SEQ":
                print("\n19: 测试机械臂顺序执行模式中, 使用延时命令")
                print(robot.set_joint_degree_synchronize(10, 10, 10, 10, 10, 10, speed_percentage=50))
                print(robot.set_time_delay(3000))
                print(robot.set_robot_end_tool(1, True))
                print(robot.set_time_delay(3000))
                print(robot.set_robot_end_tool(1, False))
                print(robot.set_time_delay(3000))
                print(robot.set_joint_degree_synchronize(20, 20, 20, 20, 20, 20, speed_percentage=50))
                print(robot.set_time_delay(3000))
                print(robot.set_robot_arm_home())
                time.sleep(3)
            
            print("\n20: 测试机械臂坐标(x,y,z,Rx,Ry,Rz)示教功能")
            robot.set_robot_cmd_mode("INT")
            coordinate_data = [[1, 1], [1, 0], [2, 1], [2, 0], 
                            [3, 1], [3, 0], [4, 1], [4, 0], 
                            [5, 1], [5, 0], [6, 1], [6, 0],
                            ]
            for each_data in coordinate_data:
                robot.set_robot_arm_coordinate_teach(each_data[0], each_data[1], 0.2, 0)
                time.sleep(3)
                robot.set_robot_arm_joint_stop()
                time.sleep(1)
            
            robot.set_robot_arm_home()
            time.sleep(2)
            
            print("\n21: 测试机械臂，沿象限方向移动")
            quadrants = [[7, 1], [7, 0], [8, 1], [8, 0],
                        [8, 1], [8, 0], [9, 1], [9, 0],
                        [10, 1], [10, 0]]
            for each_quadrant in quadrants:
                robot.set_robot_arm_coordinate_teach(each_quadrant[0], each_quadrant[1], 0.2, 0)
                time.sleep(3)
                robot.set_robot_arm_joint_stop()
                time.sleep(1)
                robot.set_robot_arm_home()
                time.sleep(1)
            
            robot.set_robot_arm_home()
            time.sleep(2)
            
            # 机械臂通讯关闭
            print("\n22: 测试机械臂通讯关闭")
            robot.end_communication()
        
    # 用户输入 crt + c 退出
    except KeyboardInterrupt:        
        robot.end_communication()