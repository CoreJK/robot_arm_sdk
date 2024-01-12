from math import pi, radians, degrees
import numpy as np
from roboticstoolbox import DHRobot, RevoluteMDH
from spatialmath import SE3
from spatialmath.base import rpy2tr


class Mirobot(DHRobot):
    """比邻星机械臂模型"""

    def __init__(self):
        L1 = RevoluteMDH(
            alpha=0,
            a=0,
            d=0.1435,
            qlim=[radians(-165), radians(165)],
            )
        L2 = RevoluteMDH(
            alpha=-pi/2, 
            a=0.02969,
            d=0, 
            offset=-pi/2,
            qlim=[radians(-90), radians(90)],
            )
        L3 = RevoluteMDH(
            alpha=0,
            a=0.16072,
            d=0,
            # offset=-pi/2,
            qlim=[radians(-60), radians(60)],
            )
        L4 = RevoluteMDH(
            alpha=-pi/2,
            a=0.02,
            d=0.23837,
            # offset=pi/2,
            qlim=[radians(-150), radians(170)],
            )
        L5 = RevoluteMDH(
            alpha=pi/2, 
            a=0,
            d=0,
            offset=pi/2,
            qlim=[radians(-30), radians(210)],
            )
        L6 = RevoluteMDH(
            alpha=pi/2,
            a=0,
            d=-0.07079, 
            qlim=[radians(-90), radians(180)])
        
        super().__init__(
            [L1, L2, L3, L4, L5, L6],
            name="Blinx_six_arm_robot",
            manufacturer="RenWeiMing"
        )
        
        self._MYCONFIG = np.array([1, 2, 3, 4, 5, 6])
        self.qr = np.array([radians(150), radians(70), radians(45), radians(150), radians(10), radians(0)])
        self.qz = np.array([radians(0), radians(0), radians(0), radians(0), radians(0), radians(0)])
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
    rs_ik = []
    for i, _ in enumerate(range(10)):
        R_T = SE3([x, y, z]) * rpy2tr([Rz, Ry, Rx], unit='deg')
        sol = mirobot.ikine_LM(R_T, joint_limits=True)

        def get_value(number):
            res = round(degrees(number), 2)
            return res

        print(f"第{i + 1}次：", list(map(get_value, sol.q)))
        rs_ik.append(list(map(get_value, sol.q)))
    
    # 统计出逆解数据列表数据中，指定数据出现的次数
    # 指定的数据为 [150.0, 70.0, 45.0, 150.0, 10.0, 0.0]
    rs_ik  # Assuming rs_ik is the inverse solution data list
    specified_data = [150.0, 70.0, 45.0, 150.0, 10.0, 0.0]
    occurrences = rs_ik.count(specified_data)
    print("Occurrences:", occurrences)
    
    # 机械臂画图
    mirobot.plot(mirobot.qz, block=True)
    
