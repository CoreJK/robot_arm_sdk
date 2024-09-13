# -*- coding: utf-8 -*-
# 测试 SDK 控制机械臂功能的代码
import time
import json
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from blinx_robots.robot_arm_interface import BlxRobotArm
from blinx_robots.robot_arm_communication import SocketCommunication
from blinx_robots._log import logger, set_stream_level, disable_logging

set_stream_level('WARNING')

# 民族舞动作
actions = {
    "1": [45, -70, 45, 0, -90, 0, 100],
    "2": [45, -70, 45, 180, -180, 0, 100],
    "3": [45, -70, 45, 180, -90, 0, 100],
    "4": [0, -70, 45, 180, -90, 0, 100],
    "5": [0, 0, 0, 0, 0, 0, 100],
    "6": [0, 0, -90, 0, -90, 0, 30],
    "7": [0, -70, 45, 0, 0, 0, 100],
    "8": [130, -70, 45, 0, 0, 0, 100],
    "9": [-130, -70, 45, 0, 0, 0, 100],
    "10": [0, 0, 0, 0, 0, 0, 100],
}

# 现代舞动作
actions_2 = {
    "1": [45, -60, 45, 180, -90, 90, 100],
    "2": [-45, 60, -45, 180, -90, 0, 100],
    "3": [-45, 60, -45, 180, 0, 0, 100],
    "4": [0, 0, -45, 0, 0, 0, 100],
    "5": [0, -45, 90, 0, 0, 0, 100],
    "6": [0, -45, 90, 180, 0, 0, 100]
}

# 霹雳舞
actions_3 = {
    "1": [0, 80, -90, 0, -90, 0, 60],
    "2": [0, 80, -90, 0, -180, 0, 100],
    "3": [45, -85, 45, 90, -90, 0, 80],
    "4": [-45, -85, 45, 90, -90, 0, 90],
    "5": [45, 0, -90, 0, -90, 0, 60],
    "6": [-120, 0, -90, 0, -90, 0, 100],
    "7": [0, -80, 45, 0, 0, 0, 100],
    "8": [-100, -80, 45, 0, 0, 0, 100],
    "9": [100, -80, 45, 0, 0, 0, 100],
    "10": [120, 0, -90, 0, -90, 0, 60],
    "11": [-120, 0, -90, 0, -90, 0, 60]
}

# 古典舞
actions_4 = {
    "1": [0.0, 35.0, 0.0, 0.0, -45.0, 0.0, 70.0],
    "2": [0.0, 15.0, 0.0, 0.0, -27.9, 0.0, 70.0],
    "3": [0.0, -45.0, 17.4, 0.0, -58.0, 0.0, 70.0],
    "4": [0.0, -28.5, 38.0, 0.0, -103.0, 0.0, 70.0],
    "5": [0.0, -28.5, 10.0, 0.0, -140.0, 0.0, 70.0],
    "6": [0.0, -1.6, 10.0, 0.0, -102.5, 0.0, 70.0],
    "7": [0.0, 18.4, -35.0, 0.0, -127.0, 0.0, 70.0],
    "8": [0.0, -1.6, -45.0, 0.0, -91.3, 0.0, 70.0],
    "9": [0.0, 8.4, -19.7, 0.0, -61.4, 0.0, 70.0],
    "10": [0.0, -28.5, 38.0, 0.0, -103.0, 0.0, 70.0],
    "11": [0.0, 32.0, -54.5, 0.0, -48.0, 0.0, 70.0],
    "12": [0.0, 12.0, -54.5, 0.0, -32.9, 0.0, 70.0],
    "13": [80.0, -47.6, 34.5, 90.0, -87.0, 0.0, 70.0],
    "14": [0.0, -47.6, 34.5, 0.0, -68.9, 0.0, 70.0],
    "15": [-40.0, -47.6, 34.5, -90.0, -124.0, 0.0, 70.0],
    "16": [-40.0, -17.1, 24.5, 0.0, -82.0, 0.0, 70.0],
    "17": [40.0, -37.1, 4.5, 90.0, -52.0, 0.0, 70.0],
    "18": [40.0, -37.1, 35.3, 0.0, -85.0, 0.0, 70.0],
    "19": [-40.0, -12.8, 4.6, -90.0, -115.0, 0.0, 70.0],
    "20": [-80.0, -22.8, 44.8, 0.0, -125.0, 0.0, 70.0],
    "21": [-85.0, -22.8, 44.9, 0.0, -125.0, 0.0, 70.0],
    "22": [-85.0, -32.8, 44.9, 0.0, -125.0, 0.0, 70.0],
    "23": [0.0, -32.8, 44.9, 90.0, -125.0, 0.0, 70.0],
    "24": [80.0, -32.8, 44.9, 0.0, -125.0, 0.0, 70.0],
    "25": [40.8, -11.0, 35.0, 0.0, -174.5, 0.0, 70.0],
    "26": [0.3, -59.3, 15.0, 0.0, -44.5, 0.0, 70.0],
    "27": [39.5, -69.3, 35.0, 0.0, -54.5, 0.0, 70.0],
    "28": [87.0, -69.3, 35.0, 0.0, -54.5, 0.0, 70.0],
    "29": [87.0, -69.5, 25.0, 0.0, -50.0, 0.0, 70.0],
    "30": [-73.0, -59.5, 15.0, 0.0, 0.0, 0.0, 70.0],
    "31": [0.0, -59.5, 15.0, 0.0, 0.0, 0.0, 70.0],
    "32": [0.0, -29.1, 16.0, 0.0, -70.0, 0.0, 70.0],
    "33": [0.0, -28.5, 38.0, 0.0, -103.0, 0.0, 70.0],
    "34": [0.0, -28.5, 10.0, 0.0, -50.0, 0.0, 70.0],
    "35": [0.0, 33.7, 10.0, 0.0, -140.0, 0.0, 70.0],
    "36": [0.0, -28.5, 38.0, 0.0, -103.0, 0.0, 70.0],
    "37": [0.0, -38.5, -32.0, -90.0, -55.5, 0.0, 70.0],
    "38": [0.0, -38.5, 18.9, 0.0, -75.5, 0.0, 70.0],
    "39": [0.0, -61.5, -24.0, 0.0, -5.2, 0.0, 70.0],
    "40": [0.0, -41.5, -44.0, 0.0, -5.4, 0.0, 70.0],
    "41": [0.0, -61.5, -24.0, -90.0, -5.2, 0.0, 70.0],
    "42": [0.0, -41.5, -44.0, 0.0, -5.4, 0.0, 70.0],
    "43": [0.0, -31.5, -54.0, -90.0, -55.4, 0.0, 70.0],
    "44": [0.0, -21.5, -59.0, 0.0, -55.4, 0.0, 70.0],
    "45": [0.0, 3.5, -59.0, 0.0, -85.4, 0.0, 70.0],
    "46": [25.0, 3.5, -59.0, 90.0, -56.0, 0.0, 70.0],
    "47": [-45.0, 13.5, -39.0, 0.0, -56.0, 0.0, 70.0],
    "48": [0.0, -16.5, -59.0, 0.0, -56.0, 0.0, 70.0],
    "49": [0.0, -36.5, -59.0, 0.0, -76.0, 0.0, 70.0],
    "50": [0.0, -46.5, -59.0, 90.0, -46.0, 0.0, 70.0],
    "51": [0.0, 18.4, -59.0, 0.0, -56.0, 0.0, 70.0],
    "52": [0.0, 34.7, -59.0, 0.0, -136.0, 0.0, 70.0],
    "53": [0.0, 18.4, -39.0, 0.0, -56.0, 0.0, 70.0],
    "54": [0.0, 34.7, -59.0, 0.0, -136.0, 0.0, 70.0],
    "55": [0.0, -28.4, -18.5, 0.0, -64.1, 0.0, 60.0],
    "56": [0.0, -14.6, 24.3, 0.0, -150.0, 0.0, 60.0],
    "57": [0.0, -28.4, 29.0, 0.0, -64.1, 0.0, 60.0],
    "58": [0.0, -14.6, 16.8, 0.0, -150.0, 0.0, 60.0],
    "59": [0.0, -28.4, 29.0, 0.0, -64.1, 0.0, 60.0],
    "60": [0.0, 0.0, 16.8, 0.0, -150.0, 0.0, 60.0]
}

all_actions = {
    # 民族舞动作
    "1": [45, -70, 45, 0, -90, 0, 100],
    "2": [45, -70, 45, 180, -180, 0, 100],
    "3": [45, -70, 45, 180, -90, 0, 100],
    "4": [0, -70, 45, 180, -90, 0, 100],
    "5": [0, 0, 0, 0, 0, 0, 100],
    "6": [0, 0, -90, 0, -90, 0, 30],
    "7": [0, -70, 45, 0, 0, 0, 100],
    "8": [130, -70, 45, 0, 0, 0, 100],
    "9": [-130, -70, 45, 0, 0, 0, 100],
    "10": [0, 0, 0, 0, 0, 0, 100],

    # 现代舞动作
    "11": [45, -60, 45, 180, -90, 90, 100],
    "12": [-45, 60, -45, 180, -90, 0, 100],
    "13": [-45, 60, -45, 180, 0, 0, 100],
    "14": [0, 0, -45, 0, 0, 0, 100],
    "15": [0, -45, 90, 0, 0, 0, 100],
    "16": [0, -45, 90, 180, 0, 0, 100],

    # 霹雳舞动作
    "17": [0, 80, -90, 0, -90, 0, 60],
    "18": [0, 80, -90, 0, -180, 0, 100],
    "19": [45, -85, 45, 90, -90, 0, 80],
    "20": [-45, -85, 45, 90, -90, 0, 90],
    "21": [45, 0, -90, 0, -90, 0, 60],
    "22": [-120, 0, -90, 0, -90, 0, 100],
    "23": [0, -80, 45, 0, 0, 0, 100],
    "24": [-100, -80, 45, 0, 0, 0, 100],
    "25": [100, -80, 45, 0, 0, 0, 100],
    "26": [120, 0, -90, 0, -90, 0, 60],
    "27": [-120, 0, -90, 0, -90, 0, 60],
    "28": [0, 0, 0, 0, 0, 0, 60]
}



def test_unit(host, port):
    while True:
        # 连接机械臂
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

def test_dance(host, port, action: dict, start_barrier=None):
    start_barrier.wait()
    socket_communication = SocketCommunication(host=host, port=port)
    robot_arm = BlxRobotArm(socket_communication)
    robot_arm.start_communication()
    robot_arm.set_robot_cmd_mode("INT")
    
    start_barrier.wait()
    robot_arm.set_robot_arm_init()
    start_barrier.wait()
    
    for key, params in action.items():
        robot_arm.set_joint_degree_synchronize(*params[:6], speed_percentage=params[6])
        start_barrier.wait()
        # if action_status:
            # logger.warning(f"Action {key} executed successfully.")
        # else:
            # logger.warning(f"Action {key} failed.")
    
    # robot_arm.set_joint_degree_by_number(1, 50, 60)
    # robot_arm.set_joint_degree_by_number(5, 50, 30)
    robot_arm.set_robot_arm_home()
    robot_arm.end_communication()
    
if __name__ == "__main__":
    test_machine = [('192.168.10.201', 4196), ('192.168.10.202', 4196), ('192.168.10.203', 4196), ('192.168.10.204', 4196)]
    # test_machine = [('192.168.10.202', 4196)]
    task_executor = ThreadPoolExecutor(max_workers=4)
    barrier = Barrier(len(test_machine))
    
    for each_machine in test_machine:
        task_executor.submit(test_dance, each_machine[0], each_machine[1], actions_4, barrier)
        
    task_executor.shutdown(wait=True)
    
    # p = Pool(4)
    # for each_machine in test_machine:
    #     p.apply_async(test_dance, args=(each_machine[0], each_machine[1], actions_4))
        
    # print('Waiting for all subprocesses done...')
    # p.close()
    # p.join()
    # print('All subprocesses done.')