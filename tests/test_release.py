# -*- coding: utf-8 -*-
# 测试 SDK 控制机械臂功能的代码
import time
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from blinx_robots.robot_arm_interface import BlxRobotArm
from blinx_robots.robot_arm_communication import SocketCommunication

logging.basicConfig(filename='OpenR6_test.log', level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")


def test_unit(host, port, start_barrier, test_loop_times=1):
    start_barrier.wait()
    # 连接机械臂
    socket_communication = SocketCommunication(host, port)
    robot = BlxRobotArm(socket_communication)
                
    # 机械臂通讯连接
    logging.info("\n1: 测试机械臂通讯连接")
    robot.start_communication()
    
    for loop_time in range(test_loop_times):
        logging.info(f"\n第 {loop_time + 1} 次测试")
        for mode in ['INT', 'SEQ']:
            # 获取机械臂的命令执行模式
            logging.info("\n2: 测试机械臂命令执行模式")
            robot_cmd_model = json.loads(robot.get_robot_cmd_mode()).get('data') 
            logging.info(f"机械臂的命令执行模式: {robot_cmd_model}")
                
            # 设置机械臂的命令模式
            logging.info("\n3: 测试机械臂命令执行模式设置")
            robot.set_robot_cmd_mode(mode)
            time.sleep(1)
                
            # 机械臂初始化，将机械臂关节角度归零
            logging.info("\n4: 测试机械臂初始化")
            logging.info(robot.set_robot_arm_init())
            time.sleep(12)
                
            # 设置机械臂单个关节角度
            logging.info("\n6: 测试机械臂单个关节角度设置")
            logging.info(robot.set_joint_degree_by_number(1, 90, 30))
            time.sleep(2)
            logging.info(robot.set_joint_degree_by_number(1, 90, -30))
            time.sleep(2)
            logging.info(robot.set_joint_degree_by_number(2, 90, 30))
            time.sleep(2)
            logging.info(robot.set_joint_degree_by_number(2, 90, -30))
            time.sleep(2)
            logging.info(robot.set_joint_degree_by_number(3, 90, 30))
            time.sleep(2)
            logging.info(robot.set_joint_degree_by_number(3, 90, -30))
            time.sleep(2)
            logging.info(robot.set_joint_degree_by_number(4, 90, 30))
            time.sleep(2)
            logging.info(robot.set_joint_degree_by_number(4, 90, -30))
            time.sleep(2)
            logging.info(robot.set_joint_degree_by_number(5, 90, 30))
            time.sleep(2)
            logging.info(robot.set_joint_degree_by_number(5, 90, -30))
            time.sleep(2)
            logging.info(robot.set_joint_degree_by_number(6, 90, 30))
            time.sleep(2)
            logging.info(robot.set_joint_degree_by_number(6, 90, -30))
            time.sleep(2)
                
                
            # 设置机械臂所有关节角度协同运动
            logging.info("\n13: 测试机械臂所有关节角度协同运动")
            logging.info(robot.set_joint_degree_synchronize(10, 10, 10, 10, 10, 10, speed_percentage=50))
            time.sleep(2)
            
            # 机械臂回零
            robot.set_robot_arm_home()
            time.sleep(2)
                
    # 机械臂通讯关闭
    logging.info("\n22: 测试机械臂通讯关闭")
    robot.end_communication()

if __name__ == "__main__":
    # 添加需要测试的机器 IP 和端口，多个机器以元组的形式添加 ('ip', 端口号)，逗号隔开
    test_machine = [('192.168.10.105', 4197), ('192.168.10.110', 4197)]
    task_executor = ThreadPoolExecutor(max_workers=len(test_machine))  
    barrier = Barrier(len(test_machine))
    
    for each_machine in test_machine:
        robot_arm_ip = each_machine[0]
        robot_arm_port = each_machine[1]
        action_loop_time = 3  # 希望机械臂执行的动作次数，默认为一次
        task_executor.submit(test_unit, robot_arm_ip, robot_arm_port, barrier, test_loop_times=action_loop_time)
        
    task_executor.shutdown(wait=True)  # 等待所有线程执行完后，关闭线程池