import time
import json
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

from blinx_robots.robot_arm_communication import SocketCommunication
from blinx_robots._log import logger


class BlxRobotArm(object):
    """比邻星六轴机械臂 API"""

    def __init__(self, communication_strategy):
        self.thread_work_flag = True
        self.robot_cmd_model = "SEQ"
        self.recv_data_buffer = Queue()
        self.command_queue = Queue()
        self.task_executor = ThreadPoolExecutor(max_workers=10)
        self.communication_strategy = communication_strategy

    def set_communication_strategy(self, communication_strategy) -> None:
        """设置机械臂的不同连接方式

        :param communication_strategy: 机械臂的不同连接对象, 对应有线、无线连接、蓝牙等
        :return: None
        """
        self.communication_strategy = communication_strategy
    
    def start_communication(self) -> None:
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
        
    def end_communication(self) -> None:
        """机械臂结束连接"""
        # todo 不同的连接策略，关闭连接的方式可能不同
        logger.warning("机械臂通讯关闭!")
        self.thread_work_flag = False
    
    def command_sender(self) -> None:
        """发送到机械臂命令线程"""
        # 不同的连接策略，发送，接收命令的方式可能不同
        while self.thread_work_flag:
            time.sleep(0.1)
            if not self.command_queue.empty():
                try:
                    with self.communication_strategy.connect() as client:
                        command = self.command_queue.get()
                        logger.debug(f"发送命令: {command.strip()}")
                        client.sendall(command.encode('utf-8'))
                except Exception as e:
                    logger.error(f"发送命令失败: {e}")
                    self.thread_work_flag = False
    
    def command_receiver(self) -> None:
        """接收机械臂返回信息的线程"""
        try:
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
        except Exception as e:
            logger.error(f"接收数据失败: {e}")
            self.thread_work_flag = False
    
    def set_robot_arm_init(self) -> str:
        """机械臂初始化，将机械臂关节角度归零
        
        :return success: {"command": "set_joint_initialize", "status": "true"}
        :return failed: {"command": "set_joint_initialize", "status": "false"}
        """
        logger.info("机械臂初始化!")
        robot_arm_init_status = self.task_executor.submit(self.get_command_response, "set_joint_initialize")
        
        payload = [0]
        command = json.dumps({"command": "set_joint_initialize", "data": payload}).replace(' ', "").strip() + '\r\n'
        self.command_queue.put(command)
        
        robot_arm_init_status_result = json.loads(robot_arm_init_status.result()).get('data')
        if robot_arm_init_status_result == 'true':
            return json.dumps({"command": "set_joint_initialize", "status": True})
        else:
            return json.dumps({"command": "set_joint_initialize", "status": False})
        
    def set_joint_degree_by_number(self, joint_number: int, speed_percentage: int, joint_degree: float) -> str:
        """设置指定的机械臂关节角度
        
        :param joint_number: 机械臂关节编号 1~6
        :param speed_percentage: 机械臂关节运动速度百分比 1~100
        :param joint_degree: 机械臂关节角度, 单位:度
        
        :return success: {"command": "set_joint_angle", "status": "true"}
        :return failed: {"command": "set_joint_angle", "status": "false"}
        """
        get_command_response_status = self.task_executor.submit(self.get_command_response, "move_in_place")
        payload = [joint_number, speed_percentage, joint_degree]
        command = json.dumps({"command": "set_joint_angle", "data": payload}).replace(' ', "").strip() + '\r\n'
        self.command_queue.put(command)
        
        get_command_response_status_result = json.loads(get_command_response_status.result()).get('data')
        if get_command_response_status_result == 'true':
            return json.dumps({"command": "set_joint_angle", "status": True})
        else:
            return json.dumps({"command": "set_joint_angle", "status": False})
    
    def set_robot_arm_home(self) -> str:
        """机械臂回零
        
        :return success: {"command": "set_robot_arm_home", "status": "true"}
        :return failed: {"command": "set_robot_arm_home", "status": "false"}
        """
        robot_arm_to_home_status = self.task_executor.submit(self.get_command_response, "move_in_place")
        command = json.dumps({"command": "set_joint_angle_all", "data": [100, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}).replace(' ', "").strip() + '\r\n'
        self.command_queue.put(command)
        logger.warning("机械臂回零!")
        
        robot_arm_to_home_status_result = json.loads(robot_arm_to_home_status.result()).get('data')
        if robot_arm_to_home_status_result == 'true':
            return json.dumps({"command": "set_robot_arm_home", "status": True})
        else:
            return json.dumps({"command": "set_robot_arm_home", "status": False})
    
    def set_joint_degree_synchronize(self, *args, speed_percentage: int = 50) -> str:
        """设置机械臂所有关节角度
        
        :param *args: 机械臂所有关节的角度 q1, q2, q3, q4, q5, q6, 单位:度
        :param speed_percentage: 机械臂关节运动速度百分比 1~100
        
        :return success: {"command": "set_joint_angle_all_time", "status": "true"}
        :return failed: {"command": "set_joint_angle_all_time", "status": "false"}
        """
        if len(args) == 6:
            set_joint_angle_all_time_status = self.task_executor.submit(self.get_command_response, "move_in_place")
            joints_degree = list(args)
            payload = [speed_percentage]
            payload.extend(joints_degree)
            command = json.dumps({"command": "set_joint_angle_all_time", "data": payload}).replace(' ', "").strip() + '\r\n'
            self.command_queue.put(command)
            
            set_joint_angle_all_time_status_result = json.loads(set_joint_angle_all_time_status.result()).get('data')
            if set_joint_angle_all_time_status_result == 'true':
                return json.dumps({"command": "set_joint_angle_all_time", "status": True})
            else:
                return json.dumps({"command": "set_joint_angle_all_time", "status": False})
        else:
            logger.error("关节超出范围!")
            return json.dumps({"command": "set_joint_angle_all_time", "status": False})
    
    def set_robot_arm_joint_stop(self) -> str:
        """机械臂关节停止运动, 与紧急停止不同，不需要重新初始化

        :return success: {"command": "set_joint_stop", "status": "true"}
        """
        with self.communication_strategy.connect() as client:
            command = json.dumps({"command": "set_joint_stop", "data": [0]}).replace(' ', "").strip() + '\r\n'
            client.send(command.encode('utf-8'))
            logger.warning("机械臂停止!")
        return json.dumps({"command": "set_robot_arm_joint_stop", "status": True})
    
    def set_robot_arm_emergency_stop(self) -> str:
        """机械臂紧急停止
        
        :return success: {"command": "set_joint_emergency_stop", "status": "true"}
        """
        # 需要立即执行的命令，不需要等待命令执行结果, 也不通过命令发送线程发送
        with self.communication_strategy.connect() as client:
            command = json.dumps({"command": "set_joint_emergency_stop", "data": [0]}).replace(' ', "").strip() + '\r\n'
            client.send(command.encode('utf-8'))
            logger.warning("机械臂紧急停止!")
        return json.dumps({"command": "set_joint_emergency_stop", "status": True})
    
    def set_robot_end_tool(self, io: int, status) -> str:
        """设置机械臂末端工具状态
        
        :param io: 机械臂末端工具编号, 1: 吸盘、2: 电动夹爪、3: 柔性夹爪
        :param status: 
             - 编号为 1: True: 打开, False: 关闭
             - 编号为 2: 0 ~ 100 整数值
             - 编号为 3: True: 吹气，False: 吸气
        
        :return success: {"command": "set_end_tool", "status": true}
        """
        with self.communication_strategy.connect() as client:
            command = json.dumps({"command": "set_end_tool", "data": [io, status]}).replace(' ', "").strip() + '\r\n'
            client.send(command.encode('utf-8'))
        return json.dumps({"command": "set_end_tool", "status": True})
    
    def set_robot_io_status(self, io: int, status: bool) -> str:
        """设置机械臂扩展 IO 口状态
        
        :param io: 机械臂 IO 口编号, 1~4
        :param status: 机械臂 IO 口状态, True:打开, False:关闭
        
        :return success: {"command": "set_io_status", "status": true}
        :return failed: {"command": "set_io_status", "status": false}
        """
        io_status = self.task_executor.submit(self.get_command_response, "set_robot_io_interface")
        command = json.dumps({"command": "set_robot_io_interface", "data": [io, status]}).replace(' ', "").strip() + '\r\n'
        self.command_queue.put(command)
        io_status_result = json.loads(io_status.result()).get('data')
        if io_status_result == 'true':
            return json.dumps({"command": "set_io_status", "status": True})
        else:
            return json.dumps({"command": "set_io_status", "status": False})
    
    def set_time_delay(self, delay_time: int) -> str:
        """设置机械臂命令之间执行延时时间
        
        在顺序执行模式中, 可以通过该延时命令, 控制机械臂命令之间的执行时间间隔
        
        :return success: {"command": "set_time_delay", "status": true}
        :return failed: {"command": "set_time_delay", "status": false}
        """
        # 判断当前的命令执行模式
        if self.robot_cmd_model == "SEQ":
            # 限制延时时间范围
            if 0 <= delay_time <= 3000:
                # 获取命令执行结果
                command = json.dumps({"command": "set_time_delay", "data": [delay_time]}).replace(' ', "").strip() + '\r\n'
                self.command_queue.put(command)
                return json.dumps({"command": "set_time_delay", "status": True})
            else:
                logger.error("延时时间超出范围!")
                return json.dumps({"command": "set_time_delay", "status": False})
        else:
            logger.error("INT 顺序模式不支持设置延时时间!")
            return json.dumps({"command": "set_time_delay", "status": False})
            
    def set_robot_cmd_mode(self, mode: str = "SEQ") -> str:
        """设置机械臂命令执行模式
            
        :params mode: SEQ(顺序执行模式)、INT(立即执行模式)
        :return success: {"command": "set_robot_mode", "status": true}
        :return failed: {"command": "set_robot_mode", "status": false}
        """
        set_cmd_mode_thread = self.task_executor.submit(self.get_command_response, "set_robot_mode")
        
        command = json.dumps({"command": "set_robot_mode", "data": [mode]}).replace(' ', "").strip() + '\r\n'
        self.command_queue.put(command)
        
        set_cmd_mode_status = json.loads(set_cmd_mode_thread.result()).get('data')
        logger.debug(f"机械臂命令模式设置结果: {set_cmd_mode_status}")
        if set_cmd_mode_status == 'true':
            logger.warning(f"机械臂命令执行模式设置成功!")
            cmd_mode_status = json.loads(self.get_robot_cmd_mode()).get('data')
            self.robot_cmd_model = cmd_mode_status  # 更新机械臂对象的命令执行模式
            logger.warning(f"机械臂当前的命令执行模式: {self.robot_cmd_model}")
            return json.dumps({"command": "set_robot_mode", "status": True})
        else:
            logger.error(f"机械臂命令执行模式设置失败!")
            return json.dumps({"command": "set_robot_mode", "status": False})

    def set_robot_arm_coordinate(self, *args, speed_percentage: int = 50) -> str:
        """通过末端工具坐标与姿态，控制机械臂关节运动
        
        :param *args: 机械臂末端工具坐标与姿态: x, y, z, Rx, Py, Yz
        :param speed_percentage: 机械臂关节运动速度百分比 1~100
        
        :return success: {"command": "set_joint_degree_by_coordinate", "status": true}
        :return failed: {"command": "set_joint_degree_by_coordinate", "status": false}
        """
        # 通过末端工具坐标控制机械臂运动
        x, y, z, Rx, Py, Yz = args
        logger.info("坐标控制机械臂关节运动!")
        set_robot_arm_coordinate_thread = self.task_executor.submit(self.get_command_response, "set_coordinate")
        
        command = json.dumps({"command": "set_coordinate", "data": [speed_percentage, x, y, z, Rx, Py, Yz]}).replace(' ', "").strip() + '\r\n'
        self.command_queue.put(command)
        
        set_cmd_mode_status = json.loads(set_robot_arm_coordinate_thread.result()).get('data')
        if set_cmd_mode_status == 'true':
            logger.info("坐标控制机械臂关节运动成功!")
            return json.dumps({"command": "set_robot_arm_coordinate", "status": True})
        else:
            logger.error("坐标控制机械臂关节运动失败!")
            return json.dumps({"command": "set_robot_arm_coordinate", "status": False})

    def set_robot_arm_coordinate_teach(self, axis: int, direction: int, speed: float, distance: float) -> str:
        """机械臂坐标示教, 可适配摇杆以及按钮长按控制
        
        :param int axis: 要移动的坐标轴或象限: 1-6:(X,Y,Z,RX,RY,RZ), 7-10: (1到4象限方向)
        :param int direction: 坐标的方向: 0 负方向 1正方向
        :param float speed: 插补步长 mm (建议: 0.1~0.3)
        :param float distance: 运动距离 mm 或度, 0 为持续运动
        :return str: {"command": "set_coordinate_teach", "status": True}
        """
        with self.communication_strategy.connect() as client:
            command = json.dumps({"command": "set_coordinate_teach", "data": [axis, direction, speed, distance]}).replace(' ', "").strip() + '\r\n'
            client.send(command.encode('utf-8'))
            logger.warning("机械臂示教中...")
            logger.debug(f"{command}")
        return json.dumps({"command": "set_robot_arm_coordinate_teach", "status": True})
    
    def get_joint_degree_all(self) -> dict:
        """获取机械臂所有关节角度
        
        :return: {"command": "get_joint_angle_all", "data": [10, 20, 30, 40, 50, 60]}
        """
        before_joint_data_temp = {}
        with self.communication_strategy.connect() as client:
            command = json.dumps({"command": "get_joint_angle_all"}).replace(' ', "").strip() + '\r\n'
            client.sendall(command.encode('utf-8'))
            try:
                recv_data = json.loads(client.recv(1024).decode('utf-8'))
                if recv_data.get('return') == 'get_coordinate':
                    return before_joint_data_temp
                else:
                    before_joint_data_temp = recv_data  # 保留最后一次的关节角度数据
            except json.JSONDecodeError:
                logger.exception("获取机械臂关节角度失败!")
                # 失败后发送最上一次的角度数据
                return before_joint_data_temp
        return recv_data
    
    def get_robot_cmd_mode(self) -> str:
        """获取机械臂命令执行模式
        
        :return: {"command": "get_robot_mode", "data": "SEQ"}
        """
        robot_cmd_mode = self.task_executor.submit(self.get_command_response, "get_robot_mode")
        get_cmd_mode_payload = json.dumps({"command": "get_robot_mode"}).replace(' ', "") + '\r\n'
        self.command_queue.put(get_cmd_mode_payload)
        return robot_cmd_mode.result()
             
    def get_robot_coordinate(self) -> str:
        """获取机械臂正解
        
        :return success: {"command": "get_positive_solution", "data": [x, y, z, Rx, Py, Yz]}
        :return failed: {"command": "get_positive_solution", "data": []}
        """
        # 计算机械臂正解
        before_coordinate_data_temp = {}
        with self.communication_strategy.connect() as client:
            command = json.dumps({"command": "get_coordinate"}).replace(' ', "").strip() + '\r\n'
            client.sendall(command.encode('utf-8'))
            try:
                recv_data = json.loads(client.recv(1024).decode('utf-8')).get('data')
                x, y, z = recv_data[:3]
                Rx, Py, Yz = recv_data[3:]
                positive_solution = json.dumps({"command": "get_positive_solution", "data": [x, y, z, Rx, Py, Yz]})
                logger.debug(f"机械臂坐标: {positive_solution}")
                
                before_coordinate_data_temp = recv_data  # 保留最后一次的关节角度数据
                return positive_solution
            except json.JSONDecodeError:
                logger.exception("获取机械臂坐标与姿态失败!")
                # 失败后发送最上一次的坐标与姿态数据
                return before_coordinate_data_temp
       
    def get_command_response(self, command_name=None) -> str:
        """获取机械臂命令执行结果"""
        get_command_response = False
        while not get_command_response:
            time.sleep(0.1)
            if not self.recv_data_buffer.empty():
                data = self.recv_data_buffer.get()
                if command_name in data:
                    response = data
                    get_command_response = True
                    break
                
        return response
    
    
if __name__ == "__main__":
    try:
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
        logger.warning("\n3: 测试机械臂命令执行模式设置")
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