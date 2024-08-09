# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import socket


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
        self.client_socket_list = []
    
    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.client_socket_list.append(self.client_socket)
        return self.client_socket        
    
    def __enter__(self):
        return self.connect()
    
    def __exit__(self):
        self.client_socket_list.pop().close()