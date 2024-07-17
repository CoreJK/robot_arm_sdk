from math import radians, pi
import numpy as np
from roboticstoolbox import DHRobot, RevoluteMDH, RevoluteDH

    
class BlinxRobotArm(DHRobot):
    """比邻星机械臂模型"""

    def __init__(self):
        L1 = RevoluteMDH(
                        alpha = 0,
                        a = 0,
                        d = 0.1535,
                        offset = 0,
                        qlim = [radians(-140), radians(140)]
                        )
        L2 = RevoluteMDH(
                        alpha = -pi / 2,
                        a = 0.024,
                        d = 0,
                        offset = -pi / 2,
                        qlim = [radians(-70), radians(70)]
                        )
        L3 = RevoluteMDH(
                        alpha = 0,
                        a = 0.16072,
                        d = 0,
                        offset = 0,
                        qlim = [radians(-60), radians(45)]
                        )
        L4 = RevoluteMDH(
                        alpha = -pi / 2,
                        a = 0,
                        d = 0.223,
                        offset = 0,
                        qlim = [radians(-150), radians(150)]
                        )
        L5 = RevoluteMDH(
                        alpha = pi / 2,
                        a = 0,
                        d = 0,
                        offset = pi / 2,
                        qlim = [radians(-180), radians(40)]
                        )
        L6 = RevoluteMDH(
                        alpha = pi / 2,
                        a = 0,
                        d = -0.10879,
                        offset = 0,
                        qlim = [radians(-180), radians(180)]
                        )
        
        super().__init__(
            [L1, L2, L3, L4, L5, L6],
            name="Blinx_six_arm_robot",
            manufacturer="任伟明"
        )
        
        self._MYCONFIG = np.array([1, 2, 3, 4, 5, 6])
        self.qr = np.radians([0, 0, 0, 0, 0, 0])
        self.qz = np.radians([0, 0, 0, 0, 0, 0])
        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

    @property
    def MYCONFIG(self):
        return self._MYCONFIG


class BlinxRobotArmDH(DHRobot):
    """"""
    def __init__(self):
        L1 = RevoluteDH(
                        alpha = -pi / 2,
                        a = 0.024,
                        d = 0.1535,
                        offset = 0,
                        qlim=[radians(-170), radians(170)]
                        )
        L2 = RevoluteDH(
                        alpha = 0.0,
                        a = 0.16072,
                        d = 0,
                        offset = -pi / 2,
                        qlim=[radians(-70), radians(70)]
                        )
        L3 = RevoluteDH(
                        alpha = -pi / 2,
                        a = 0.0,
                        d = 0.0,
                        offset = 0,
                        qlim=[radians(-60), radians(45)]
                        )
        L4 = RevoluteDH(
                        alpha = pi / 2,
                        a = 0.0,
                        d = 0.223,
                        offset = 0,
                        qlim=[radians(-150), radians(150)]
                        )
        L5 = RevoluteDH(
                        alpha = pi / 2,
                        a = 0.0,
                        d = 0.0,
                        offset = pi / 2,
                        qlim=[radians(-180), radians(10)]
                        )
        L6 = RevoluteDH(
                        alpha = 0,
                        a = 0.0,
                        d = -0.10879,
                        offset = 0,
                        qlim=[radians(-180), radians(180)]
                        )
        
        super().__init__(
            [L1, L2, L3, L4, L5, L6],
            name="Blinx_six_arm_robot",
            manufacturer="任伟明"
        )
        
        self._MYCONFIG = np.array([1, 2, 3, 4, 5, 6])
        self.qr = np.radians([0, 0, 0, 0, 0, 0])
        self.qz = np.radians([0, 0, 0, 0, 0, 0])
        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

    @property
    def MYCONFIG(self):
        return self._MYCONFIG
