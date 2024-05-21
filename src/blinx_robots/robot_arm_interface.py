import time
import json
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from loguru import logger
from spatialmath import SE3
from spatialmath.base import rpy2tr

from blinx_robots.robot_arm_module import BlinxRobotArm
from blinx_robots.robot_arm_communication import SocketCommunication

# logger.add("logs/robot_arm_interface.log", rotation="10 MB", level="DEBUG")

class BlxRobotArm(object):
    """比邻星六轴机械臂 API"""

    def __init__(self, communication_strategy):
        self.thread_work_flag = True
        self.robot_cmd_model = "SEQ"
        self.recv_data_buffer = Queue()
        self.command_queue = Queue()
        self.blinx_robot_arm = BlinxRobotArm()
        self.task_executor = ThreadPoolExecutor(max_workers=10)
        self.communication_strategy = communication_strategy

    def set_communication_strategy(self, communication_strategy):
        """设置机械臂的不同连接方式"""
        self.communication_strategy = communication_strategy
    
    def start_communication(self):
        """机械臂开始连接"""
        try:
            # 启动发送命令线程
            logger.warning("启动发送命令线程...")
            self.task_executor.submit(self.command_sender)
            
            # 启动数据接收线程
            logger.warning("启动接收数据线程...")
            self.task_executor.submit(self.command_receiver)
            
        except Exception as e:
            logger.warning(f"机械臂连接关闭: {e}")
        
    def end_communication(self):
        """机械臂结束连接"""
        # todo 不同的连接策略，关闭连接的方式可能不同
        logger.warning("机械臂通讯关闭!")
        self.thread_work_flag = False
    
    def command_sender(self):
        """发送命令到机械臂
        :param command: 机械臂命令
        """
        # 不同的连接策略，发送，接收命令的方式可能不同
        while self.thread_work_flag:
            time.sleep(0.1)
            if not self.command_queue.empty():
                with self.communication_strategy.connect() as client:
                    command = self.command_queue.get()
                    logger.debug(f"发送命令: {command.strip()}")
                    client.sendall(command.encode('utf-8'))
    
    def command_receiver(self):
        """接收机械臂返回的数据"""
        with self.communication_strategy.connect() as client:
            while self.thread_work_flag:
                time.sleep(0.1)
                recv_data = client.recv(1024).decode('utf-8')
                # logger.debug(f"接收数据: {recv_data.strip()}")
                # 放入队列前, 将粘包的数据进行处理
                recv_data_list = list(filter(lambda s: s and s.strip(), recv_data.split('\r\n')))
                for recv_data in recv_data_list:
                    self.recv_data_buffer.put(recv_data)
                
                # 打印队列中的数据的长度, 用于调试
                # logger.debug(f"接收数据队列长度: {self.recv_data_buffer.qsize()}")
    
    def set_robot_arm_init(self) -> str:
        """机械臂初始化，将机械臂关节角度归零
        :return: {"command": "set_joint_initialize", "data": "true"}
        """
        logger.info("机械臂初始化!")
        robot_arm_init_status = self.task_executor.submit(self.get_command_response, "set_joint_initialize")
        
        payload = [0]
        command = json.dumps({"command": "set_joint_initialize", "data": payload}).replace(' ', "").strip() + '\r\n'
        self.command_queue.put(command)
        
        return robot_arm_init_status.result()
    
    def set_joint_degree_by_number(self, joint_number: int, speed_percentage: int, joint_degree: float) -> str:
        """设置指定的机械臂关节角度
        :param joint_number: 机械臂关节编号 1~6
        :param speed_percentage: 机械臂关节运动速度百分比 1~100
        :param joint_degree: 机械臂关节角度, 单位:度
        """
        status = self.task_executor.submit(self.get_command_response, "move_in_place")
        payload = [joint_number, speed_percentage, joint_degree]
        command = json.dumps({"command": "set_joint_angle", "data": payload}).replace(' ', "").strip() + '\r\n'
        self.command_queue.put(command)
        return status.result()
    
    def set_robot_arm_home(self) -> str:
        """机械臂回零
        :return: {"command": "set_joint_angle_all", "data": [100, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
        """
        robot_arm_to_home_status = self.task_executor.submit(self.get_command_response, "move_in_place")
        command = json.dumps({"command": "set_joint_angle_all", "data": [100, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}).replace(' ', "").strip() + '\r\n'
        self.command_queue.put(command)
        logger.warning("机械臂回零!")
        return robot_arm_to_home_status.result()
    
    def set_joint_degree_synchronize(self, *args, speed_percentage: int = 50) -> dict:
        """设置机械臂所有关节角度
        :param *args: 机械臂所有关节的角度 q1, q2, q3, q4, q5, q6, 单位:度
        :param speed_percentage: 机械臂关节运动速度百分比 1~100
        """
        if len(args) == 6:
            status = self.task_executor.submit(self.get_command_response, "move_in_place")
            joints_degree = list(args)
            payload = [speed_percentage]
            payload.extend(joints_degree)
            command = json.dumps({"command": "set_joint_angle_all_time", "data": payload}).replace(' ', "").strip() + '\r\n'
            self.command_queue.put(command)
            return status.result()
        else:
            logger.error("关节超出范围!")
            return json.dumps({"command": "set_joint_angle_all_time", "status": "false"})
    
    def set_robot_arm_emergency_stop(self):
        """机械臂紧急停止"""
        # 需要立即执行的命令，不需要等待命令执行结果, 也不通过命令发送线程发送
        with self.communication_strategy.connect() as client:
            command = json.dumps({"command": "set_joint_emergency_stop", "data": [0]}).replace(' ', "").strip() + '\r\n'
            client.send(command.encode('utf-8'))
            logger.warning("机械臂紧急停止!")
    
    def set_robot_end_tool(self, io: int, status: bool) -> str:
        """设置机械臂 IO 口状态
        :param io: 机械臂IO口, 1~3
        :param status: 机械臂IO口状态, True:打开, False:关闭
        """
        end_tool_status = self.task_executor.submit(self.get_command_response, "set_end_tool")
        command = json.dumps({"command": "set_end_tool", "data": [io, status]}).replace(' ', "").strip() + '\r\n'
        self.command_queue.put(command)
        return end_tool_status.result()
    
    def set_time_delay(self, delay_time: int):
        """设置机械臂命令之间执行延时时间"""
        # 判断当前的命令执行模式
        if self.robot_cmd_model == "SEQ":
            # 限制延时时间范围
            if 0 <= delay_time <= 3000:
                # 获取命令执行结果
                command = json.dumps({"command": "set_time_delay", "data": [delay_time]}).replace(' ', "").strip() + '\r\n'
                self.command_queue.put(command)
            else:
                logger.error("延时时间超出范围!")
        else:
            logger.error("INT 顺序模式不支持设置延时时间!")
    
    def set_robot_cmd_mode(self, mode="SEQ"):
        """设置机械臂命令执行模式
            SEQ: 顺序执行模式
            INT: 立即执行模式
        """
        set_cmd_mode_thread = self.task_executor.submit(self.get_command_response, "set_robot_mode")
        
        command = json.dumps({"command": "set_robot_mode", "data": [mode]}).replace(' ', "").strip() + '\r\n'
        self.command_queue.put(command)
        
        status = set_cmd_mode_thread.result()
        set_cmd_mode_status = json.loads(set_cmd_mode_thread.result()).get('data')
        logger.debug(f"机械臂命令模式设置结果: {set_cmd_mode_status}")
        if set_cmd_mode_status:
            logger.warning(f"机械臂命令执行模式设置成功!")
            cmd_mode_status = json.loads(self.get_robot_cmd_model()).get('data')
            self.robot_cmd_model = cmd_mode_status  # 更新机械臂对象的命令执行模式
            logger.warning(f"机械臂当前的命令执行模式: {self.robot_cmd_model}")
            return status
        else:
            logger.error(f"机械臂命令执行模式设置失败!")
            return status

    def set_joint_degree_by_coordinate(self, *args, speed_percentage: int = 50) -> dict:
        """通过末端工具坐标与姿态，控制机械臂关节运动
        :param *args: 机械臂末端工具坐标与姿态: x, y, z, Rx, Py, Yz
        :param speed_percentage: 机械臂关节运动速度百分比 1~100
        """
        # 通过末端工具坐标与姿态，计算机械臂逆解
        inverse_solution = json.loads(self.get_inverse_solution(*args)).get('data')
        if inverse_solution:
            # 设置机械臂关节角度
            logger.info("坐标控制机械臂关节运动!")
            self.set_joint_degree_synchronize(*inverse_solution, speed_percentage=speed_percentage)
        else:
            logger.error("获取机械臂逆解失败!")
            return json.dumps({"command": "set_coordinate_axle_all_speed", "status": "false"})

    def get_joint_degree_all(self) -> dict:
        """获取机械臂所有关节角度"""
        get_joint_degree_thread = self.task_executor.submit(self.get_command_response, "get_joint_angle_all")
        command = json.dumps({"command": "get_joint_angle_all"}).replace(' ', "").strip() + '\r\n'
        self.command_queue.put(command)
        data = json.loads(get_joint_degree_thread.result())
        return data
    
    def get_robot_cmd_model(self) -> str:
        """获取机械臂命令执行模式"""
        robot_cmd_model = self.task_executor.submit(self.get_command_response, "get_robot_mode")
        get_cmd_model_payload = json.dumps({"command": "get_robot_mode"}).replace(' ', "") + '\r\n'
        self.command_queue.put(get_cmd_model_payload)
        return robot_cmd_model.result()
             
    def get_positive_solution(self, *args, current_pose=False) -> str:
        """获取机械臂正解
        根据提供的机械臂各个关节的角度，计算出机械臂末端的位置和姿态

        :params args: 机械臂关节角度值 q1, q2, q3, q4, q5, q6, 单位:度
        :params current_pose: 是否使用当前机械臂关节角度值, 默认为 False, False 可以不用提供所有关节角度值
        """
        if current_pose:
            joint_angle_list = self.get_joint_degree_all().get('data')
        else:
            joint_angle_list = list(args)

        if joint_angle_list and len(joint_angle_list) == 6:
            # 计算机械臂正解
            arm_joint_radians = np.radians(joint_angle_list)
            translation_vector = self.blinx_robot_arm.fkine(arm_joint_radians)
            x, y, z = np.round(translation_vector.t, 3)  # 平移向量
            Rx, Py, Yz = np.round(translation_vector.rpy(order="zyx"), 3)  # 旋转角
            positive_solution = json.dumps({"command": "get_positive_solution", "data": [x, y, z, Rx, Py, Yz]})
            logger.debug(f"机械臂正解: {positive_solution}")
            return positive_solution
        else:
            logger.error("获取机械臂角度值失败!")
            positive_solution = json.dumps({"command": "get_positive_solution", "data": []})
            return positive_solution

    def get_inverse_solution(self, *args, current_pose=False) -> str:
        """获取机械臂逆解
        :params *args: 机械臂 x, y, z, Rx, Py, Yz 坐标
        :params current_pose: 是否使用当前机械臂关节角度值
        """
        if current_pose:
            positive_solution = json.loads(self.get_positive_solution(current_pose=True)).get('data')
            x, y, z, Rx, Py, Yz = positive_solution
        else:
            x, y, z, Rx, Py, Yz = list(args)

        R_T = SE3([x, y, z]) * rpy2tr([Rx, Py, Yz], order='zyx')
        sol = self.blinx_robot_arm.ikine_LM(R_T, joint_limits=True)
        if sol.success:
            inverse_result = np.round(np.degrees(sol.q), 3).tolist()
            ik_solution = json.dumps({"command": "get_inverse_kinematics", "data": inverse_result})
            logger.debug(f"机械臂逆解: {ik_solution}")
            return ik_solution
        else:
            logger.error("获取机械臂逆解失败!")
            return json.dumps({"command": "get_inverse_kinematics", "data": []})

    @logger.catch
    def get_command_response(self, command_name=None) -> str:
        """获取机械臂命令执行结果"""
        get_command_response = False
        while not get_command_response:
            time.sleep(0.1)
            # logger.warning(f"等待 {command_name} 命令响应结果...")
            if not self.recv_data_buffer.empty():
                data = self.recv_data_buffer.get()
                if command_name in data:
                    response = data
                    logger.warning(f"获取到机械臂命令执行结果: {data.strip()}")
                    get_command_response = True
                    break
                
        return response
    
    
if __name__ == "__main__":
    try:
        # 连接机械臂
        host = "192.168.10.234"
        port = 1234
        socket_communication = SocketCommunication(host, port)
        robot = BlxRobotArm(socket_communication)
        
        # 机械臂通讯连接
        logger.warning("\n1: 测试机械臂通讯连接")
        robot.start_communication()
        
        # 获取机械臂的命令执行模式
        logger.warning("\n2: 测试机械臂命令执行模式")
        robot_cmd_model = json.loads(robot.get_robot_cmd_model()).get('data') 
        logger.info(f"机械臂的命令执行模式: {robot_cmd_model}")
        
        # 设置机械臂的命令模式
        logger.warning("\n3: 测试机械臂命令执行模式设置")
        # robot.set_robot_cmd_mode("INT")
        # time.sleep(1)
        robot.set_robot_cmd_mode("SEQ")
        time.sleep(1)
        
        # 机械臂初始化，将机械臂关节角度归零
        logger.warning("\n4: 测试机械臂初始化")
        robot.set_robot_arm_init()
        time.sleep(12)
        
        # 获取机械臂关节角度
        logger.warning("\n5: 测试机械臂关节角度")
        robot.get_joint_degree_all()
        time.sleep(1)
        
        # 设置机械臂单个关节角度
        logger.warning("\n6: 测试机械臂单个关节角度设置")
        robot.set_joint_degree_by_number(1, 50, 90)
        
        # 获取机械臂所有当前关节角度
        logger.warning("\n7: 测试机械臂所有关节角度设置")
        joint_degree = robot.get_joint_degree_all().get('data')
        logger.info(f"机械臂所有关节角度: {joint_degree}")
        time.sleep(1)
        
        # 机械臂紧急停止
        logger.warning("\n8: 测试机械臂紧急停止")
        robot.set_robot_arm_emergency_stop()
        time.sleep(2)
        
        # 恢复机械臂状态
        logger.warning("\n9: 测试机械臂急停后的状态恢复上电")
        robot.set_robot_arm_init()
        time.sleep(2)
        logger.warning("\n10: 测试机械臂急停后的状态恢复")
        robot.set_robot_arm_init()
        time.sleep(12)
        
        # 设置机械臂末端工具控制
        logger.warning("\n11: 测试机械臂末端工具控制使能")
        robot.set_robot_end_tool(1, True)  # 控制气泵打开
        time.sleep(2)
        logger.warning("\n12: 测试机械臂末端工具控制掉使能")
        robot.set_robot_end_tool(1, False)  # 控制气泵关闭
        time.sleep(2)
        
        # 设置机械臂所有关节角度协同运动
        logger.warning("\n13: 测试机械臂所有关节角度协同运动")
        robot.set_joint_degree_synchronize(10, 10, 10, 10, 10, 10, speed_percentage=50)
        time.sleep(2)
        
        # 通过末端工具坐标与姿态，控制机械臂关节运动
        logger.warning("\n14: 测试通过末端工具坐标与姿态，控制机械臂关节运动")
        robot.set_joint_degree_by_coordinate(0.287, 0.0, 0.269, 0.0, -0.0, 0.0, speed_percentage=50)
        time.sleep(5)
        
        # 机械臂回零
        logger.warning("\n15: 测试机械臂回零")
        robot.set_robot_arm_home()
        time.sleep(2)
        
        # 获取机械臂正解
        logger.warning("\n16: 测试获取机械臂当前角度的, 正解")
        robot.get_positive_solution(current_pose=True)
        logger.warning("\n17: 测试获取机械臂单独计算正解")
        robot.get_positive_solution(20, 0, 0, 0, 0, 0, current_pose=False)
        
        # 获取机械臂逆解
        logger.warning("\n18: 测试获取机械臂当前角度的, 逆解")
        robot.get_inverse_solution(current_pose=True)
        logger.warning("\n19: 测试获取机械臂单独计算逆解")
        robot.get_inverse_solution(0.23, 0.084, 0.269, 20.0, -0.0, -0.0, current_pose=False)
        
        # 顺序执行模式中, 使用延时命令
        logger.warning("\n20: 测试机械臂顺序执行模式中, 使用延时命令")
        robot.set_joint_degree_synchronize(10, 10, 10, 10, 10, 10, speed_percentage=50)
        robot.set_time_delay(3000)
        robot.set_robot_end_tool(1, True)
        robot.set_time_delay(3000)
        robot.set_robot_end_tool(1, False)
        robot.set_time_delay(3000)
        robot.set_joint_degree_synchronize(20, 20, 20, 20, 20, 20, speed_percentage=50)
        robot.set_time_delay(3000)
        robot.set_robot_arm_home()
        time.sleep(3)
        
        # 机械臂通讯关闭
        logger.warning("\n21: 测试机械臂通讯关闭")
        robot.end_communication()
        
    # 用户输入 crt + c 退出
    except KeyboardInterrupt:        
        robot.end_communication()