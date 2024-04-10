import sys
import serial
import threading
import time
import json

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

        while self.running:
            # 发送命令
            command = json.dumps({"command": "get_joint_angle_all"}) + "\r\n"
            self.serial.write(command.encode('utf-8'))

            # 读取返回的数据
            if self.serial.in_waiting:
                response = self.serial.read(self.serial.in_waiting)
                try:
                    joints_data = json.loads(response.decode('utf-8')).get('data')
                    speed = list(joints_data[0])
                    left_arm = list(joints_data[1])
                    right_arm = list(joints_data[2])

                    # 将数据记录到数据文件中
                    record_flag = input("输入 1 记录当前数据: ")
                    if record_flag == '1':
                        with open('data.json', 'w') as f:
                            json.dump({"speed": speed, 
                                       "left_arm": left_arm, 
                                       "right_arm": right_arm}, f)
                    elif record_flag == 'q':
                        self.stop()
                        sys.exit(0)
                    else:
                        continue
                    
                except json.JSONDecodeError:
                    continue

            # 休眠一段时间，以防止 CPU 占用过高
            time.sleep(0.1)

    def stop(self):
        self.running = False
        if self.serial:
            self.serial.close()


if __name__ == "__main__":
    # 使用线程
    thread = SerialThread('COM4')
    thread.start()

    # 停止线程
    thread.stop()