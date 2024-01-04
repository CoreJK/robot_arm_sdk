from math import pi, radians, degrees
import numpy as np
from roboticstoolbox import DHRobot, RevoluteMDH
from spatialmath import SE3
from spatialmath.base import rpy2tr


class Mirobot(DHRobot):
    """比邻星机械臂模型"""

    def __init__(self):
        L0 = RevoluteMDH(
            d=143.5,
            qlim=[radians(-165), radians(165)],
            )
        L1 = RevoluteMDH(
            a=59.50, 
            alpha=-pi/2, 
            offset=-pi/2,
            qlim=[radians(-90), radians(90)],
            )
        L2 = RevoluteMDH(
            a=160.72,
            qlim=[radians(-60), radians(60)],
            )
        L3 = RevoluteMDH(
            d=238.67, 
            a=59.50,
            alpha=-pi/2,
            qlim=[radians(-150), radians(170)],
            )
        L4 = RevoluteMDH(
            alpha=pi/2, 
            offset=pi/2,
            qlim=[radians(-30), radians(210)],
            )
        L5 = RevoluteMDH(
            d=-70.5, 
            alpha=pi/2,
            qlim=[radians(-180), radians(180)])
        
        super().__init__(
            [L0, L1, L2, L3, L4, L5],
            name="mirobot",
            manufacturer="BLinx"
        )
        
        self._MYCONFIG = np.array([1, 2, 3, 4, 5, 6])
        self.qr = np.array([0, radians(90), radians(90), 0, 0, 0])
        self.qz = np.zeros(6)
        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

    @property
    def MYCONFIG(self):
        return self._MYCONFIG


if __name__ == "__main__":
    mirobot = Mirobot()
    print(mirobot)

    # 机械臂正运动解
    q1 = radians(150)
    q2 = radians(70)
    q3 = radians(45)
    q4 = radians(150)
    q5 = radians(10)
    q6 = radians(0)
    print("机械臂关节角度 = ", [round(degrees(i), 2) for i in [q1, q2, q3, q4, q5, q6]])
    arm_pose_degree = np.array([q1, q2, q3, q4, q5, q6])
    translation_vector = mirobot.fkine(arm_pose_degree)

    print("机械臂正解结果")
    print(translation_vector.printline(), '\n')
    x, y, z = translation_vector.t  # 平移向量
    print("x = ", round(x, 2))
    print("y = ", round(y, 2))
    print("z = ", round(z, 2))
    print('')
    Rz, Ry, Rx = map(lambda x: degrees(x), translation_vector.rpy())  # 旋转角
    print("Rz = ", round(Rz, 2))
    print("Ry = ", round(Ry, 2))
    print("Rx = ", round(Rx, 2))
    print("")
    
    # 机器人逆运动解
    # 给出符合逆解条件的末端坐标 T 值
    print("机械臂逆解结果")
    R_T = SE3([round(x, 2), round(y, 2), round(z, 2)]) * rpy2tr([round(Rz, 2), round(Ry, 2), round(Rx, 2)], unit='deg')
    sol = mirobot.ikine_LM(R_T, joint_limits=True)

    def get_value(number):
        res = round(degrees(number), 2)
        return res

    print(list(map(get_value, sol.q)))
