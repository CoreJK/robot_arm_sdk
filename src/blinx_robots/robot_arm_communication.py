from abc import ABC, abstractmethod
import socket
from loguru import logger
from retrying import retry


class CommunicationStrategy(ABC):
    @abstractmethod
    def connect(self):
        pass
    

# 机械臂连接方式
class SocketCommunication(CommunicationStrategy):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
    
    @retry(stop_max_attempt_number=3, wait_fixed=1000)
    def connect(self):
        logger.info("正在尝试连接机械臂...")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        logger.info("连接成功!")
        return self.client_socket        