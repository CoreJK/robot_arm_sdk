# -*- coding: utf-8 -*-
# 测试 SDK 控制机械臂功能的代码
import time
import json

from blinx_robots.robot_arm_interface import BlxRobotArm
from blinx_robots.robot_arm_communication import SocketCommunication

# logger.add("robot_arm_interface.log", rotation="10 MB", level="DEBUG")

if __name__ == "__main__":
    try:
        while True:
            # 连接机械臂
            host = "192.168.10.33"
            port = 4197
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
            # robot.set_robot_cmd_mode("INT")
            # time.sleep(1)
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
            print(robot.set_joint_degree_by_coordinate(0.287, 0.0, 0.269, 0.0, -0.0, 0.0, speed_percentage=50))
            time.sleep(5)
            
            # 机械臂回零
            print("\n15: 测试机械臂回零")
            print(robot.set_robot_arm_home())
            time.sleep(2)
            
            # 获取机械臂正解
            print("\n16: 测试获取机械臂当前角度的, 正解")
            print(robot.get_positive_solution(current_pose=True))
            print("\n17: 测试获取机械臂单独计算正解")
            print(robot.get_positive_solution(20, 0, 0, 0, 0, 0, current_pose=False))
            
            # 获取机械臂逆解
            print("\n18: 测试获取机械臂当前角度的, 逆解")
            print(robot.get_inverse_solution(current_pose=True))
            print("\n19: 测试获取机械臂单独计算逆解")
            print(robot.get_inverse_solution(0.23, 0.084, 0.269, 20.0, -0.0, -0.0, current_pose=False))
            
            # 顺序执行模式中, 使用延时命令
            if robot_cmd_model == "SEQ":
                print("\n20: 测试机械臂顺序执行模式中, 使用延时命令")
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
            
            # 机械臂通讯关闭
            print("\n21: 测试机械臂通讯关闭")
            robot.end_communication()
            
    # 用户输入 crt + c 退出
    except KeyboardInterrupt:        
        robot.end_communication()
        
