import json
import time
import datetime
import threading
import logging

import serial

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class SerialThread(threading.Thread):
    def __init__(self, port, baudrate=115200, parity=serial.PARITY_NONE):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.serial = None
        self.running = False

    def run(self):
        self.serial = serial.Serial(self.port, self.baudrate, parity=self.parity)
        self.running = True
        record_datas = []

        while self.running:
            # 发送命令
            command = json.dumps({"command": "get_joint_angle_all"}) + "\r\n"
            self.serial.write(command.encode('utf-8'))

            # 读取返回的数据
            if self.serial.in_waiting:
                response = self.serial.read(self.serial.in_waiting)
                try:
                    joints_data = json.loads(response.decode('utf-8')).get('data')
                    speed = [90]
                    left_arm = joints_data[:5]
                    right_arm = joints_data[5:]

                    # 将数据记录到数据文件中
                    logging.info(f"当前数据: {response}")
                    record_flag = input("输入 1 记录当前数据: ")
                    if record_flag == '1':
                        robot_arm_pose = {"speed": speed, "left_arm": left_arm, "right_arm": right_arm}
                        record_datas.append(robot_arm_pose)
                        logging.debug(f"记录当前数据: {robot_arm_pose}")
                    elif record_flag == 'q':
                        logging.info("退出记录模式!")
                        break
                    else:
                        logging.warning("跳过当前动作记录!")
                    
                except json.JSONDecodeError:
                    logging.error("返回数据解码异常, 无法记录!")
                    
            # 休眠一段时间，以防止 CPU 占用过高
            time.sleep(0.1)

        self.save_robot_arm_pose(record_datas)

    def save_robot_arm_pose(self, record_datas):
        logging.info("开始保存机械臂动作！")
        
        file_name_prefix = input("输入文件名保存机械臂动作: ")
        with open(f'{file_name_prefix}_{datetime.datetime.strftime()}.json', 'w') as f:
            f.write(json.dumps(record_datas, indent=2))
            
        logging.info("机械臂动作保存成功!")
        self.stop()

    def stop(self):
        self.running = False
        if self.serial:
            self.serial.close()



if __name__ == "__main__":
    # 使用线程
    thread = SerialThread('COM9')
    thread.start()

    # 停止线程
    thread.stop()