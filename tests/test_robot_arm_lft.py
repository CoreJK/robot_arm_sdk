import time
import json
from loguru import logger

from blinx_robots.robot_arm_interface import BlxRobotArm
from blinx_robots.robot_arm_communication import SocketCommunication

logger.add("robot_arm_interface.log", rotation="100 MB", level="DEBUG")

if __name__ == "__main__":
    try:
        # 连接机械臂
        robot_one_host = "192.168.10.32"
        port = 1234
        socket_communication = SocketCommunication(robot_one_host, port)
        robot = BlxRobotArm(socket_communication)
        
        # 机械臂通讯连接
        logger.info("\n1: 测试机械臂通讯连接")
        robot.start_communication()
        robot_arm_test_count = 0
        
        while True:
            robot_arm_test_count += 1
            logger.warning(f"机械臂测试次数: {robot_arm_test_count}")
            # 获取机械臂的命令执行模式
            logger.info("\n2: 测试机械臂命令执行模式")
            robot_cmd_model = json.loads(robot.get_robot_cmd_mode()).get('data') 
            logger.warning(f"机械臂的命令执行模式: {robot_cmd_model}")
            
            # 设置机械臂的命令模式
            logger.info("\n3: 测试机械臂命令执行模式设置")
            logger.debug(robot.set_robot_cmd_mode("SEQ"))
            time.sleep(1)
            
            # 机械臂初始化，将机械臂关节角度归零
            logger.info("\n4: 测试机械臂初始化")
            logger.info(robot.set_robot_arm_init())
            time.sleep(12)
            
            # 测试机械臂角度控制
            logger.info("\n5: 测试机械臂角度控制")
            # logger.debug(robot.set_joint_degree_synchronize(0, 0, -92.788, 0, -100.404, 0, speed_percentage=100))
            # logger.debug(robot.set_joint_degree_synchronize(0, -86.123, -92.788, 0, -100.404, 0, speed_percentage=100))
            # logger.debug(robot.set_joint_degree_synchronize(0, 96.988, -92.788, 0, -100.404, 0, speed_percentage=100))
            # logger.debug(robot.set_joint_degree_synchronize(0, 0, -92.788, 0, -100.404, 0, speed_percentage=100))
            logger.debug(robot.set_joint_degree_synchronize(-360, -360, 360, -360, -360, -360, speed_percentage=100))
            logger.debug(robot.set_joint_degree_synchronize(360, 360, -360, 360, 360, 360, speed_percentage=100))
            logger.debug(robot.set_robot_arm_home())
            time.sleep(10)
            
    # 用户输入 crt + c 退出
    except KeyboardInterrupt:        
        robot.end_communication()
        
