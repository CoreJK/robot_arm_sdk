from math import radians, pi
import numpy as np
from roboticstoolbox import DHRobot, RevoluteMDH

    

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
                        d = 0.2205,
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
                        d = -0.045,
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


if __name__ == "__main__":
    blinx_robot_arm = BlinxRobotArm()
    print(blinx_robot_arm)

    # 机械臂画图
    blinx_robot_arm.teach(blinx_robot_arm.qz, block=True)
    
