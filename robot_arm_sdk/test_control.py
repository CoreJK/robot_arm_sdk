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
    # print(robot.set_joint_return_to_zero())
    
    # 获取机械臂关节角度
    # print(robot.get_joint_angle_all())
    
    # 设置指定的机械臂关节角度
    # print(robot.set_joint_angle(1, 50, 50))
    
    # 设置机械臂所有关节角度同时运动
    # print(robot.set_joint_angle_all_time(0, 0, 0, 0, 0, 0, speed_percentage=100))
    
    # 获取机械臂正解
    # print(robot.get_positive_solution())
    # 获取机械臂逆解
    
    # 控制IO口
    # print(robot.set_robot_io_interface(0, True))  # 打开IO口
    # print(robot.set_robot_io_interface(0, False))  # 关闭IO口
    
    
