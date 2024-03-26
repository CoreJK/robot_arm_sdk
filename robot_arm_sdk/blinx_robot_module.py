from math import radians, degrees, pi
import yaml
import numpy as np
from roboticstoolbox import DHRobot, RevoluteMDH
from spatialmath import SE3
from spatialmath.base import rpy2tr

class RobotArmConfig(object):
    """解析机械臂模型的配置文件类"""
    def __init__(self, yaml_file):
        self._config_file = yaml_file
        
    def open_yaml_config(self):
        try:
            with open(self._config_file, 'r', encoding='utf-8') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(f"打开配置文件 {self._config_file} 失败，错误信息：{e}")
        return config
    
    def get_joint_mdh_parameters(self, joint_number):
        """获取指定关节的 MDH 参数对象"""
        config = self.open_yaml_config()
        for each_joint in config:
            if each_joint.get('joint') == joint_number:
                try:
                    return RevoluteMDH(
                        alpha = self.get_joint_alpha(each_joint),
                        a = self.get_joint_a(each_joint),
                        d = self.get_joint_d(each_joint),
                        offset = self.get_joint_offset(each_joint),
                        qlim= self.get_joint_qlim(each_joint)
                    )
                except Exception as e:
                    print(f"获取关节 {joint_number} 的 MDH 参数对象失败，错误信息：{e}")
                
        
    def get_joint_alpha(self, joint_config: dict):
        """获取关节的 alpha 参数"""
        alpha_value = joint_config.get('alpha')
        if isinstance(alpha_value, (int, float)):
            joint_alpha = alpha_value
        else:
            # todo 可能存在安全问题（任意代码执行）
            # 暂时没有修复的原因是 ast.literal_eval 无法解析 -math.pi 这种表达式
            joint_alpha = eval(alpha_value)

        return joint_alpha
    
    def get_joint_a(self, joint_config: dict):
        """获取关节的 a 参数"""
        return joint_config.get('a', 0.0)
    
    def get_joint_d(self, joint_config: dict):
        """获取关节的 d 参数"""
        return joint_config.get('d', 0.0)
    
    def get_joint_offset(self, joint_config: dict):
        """获取关节的 offset 参数"""
        # offset 参数对应 MDH 配置文件中的 theta 值(关节建系时的偏移角度)
        theta_value = joint_config.get('theta')
        if isinstance(theta_value, (int, float)):
            joint_theta = theta_value
        else:
            # todo 可能存在安全问题（任意代码执行）
            # 暂时没有修复的原因是 ast.literal_eval 无法解析 -math.pi 这种表达式
            joint_theta = eval(theta_value)

        return joint_theta
    
    def get_joint_qlim(self, joint_config: dict):
        """获取关节的 qlim 参数"""
        return [radians(joint_config.get('qlim')[0]), radians(joint_config.get('qlim')[1])]
    

class Mirobot(DHRobot):
    """比邻星机械臂模型"""

    def __init__(self, robot_module_config_file):
        self.config_parser = RobotArmConfig(robot_module_config_file)
        L1 = self.config_parser.get_joint_mdh_parameters(1)
        L2 = self.config_parser.get_joint_mdh_parameters(2)
        L3 = self.config_parser.get_joint_mdh_parameters(3)
        L4 = self.config_parser.get_joint_mdh_parameters(4)
        L5 = self.config_parser.get_joint_mdh_parameters(5)
        L6 = self.config_parser.get_joint_mdh_parameters(6)
        
        super().__init__(
            [L1, L2, L3, L4, L5, L6],
            name="Blinx_six_arm_robot",
            manufacturer="RenWeiMing"
        )
        
        self._MYCONFIG = np.array([1, 2, 3, 4, 5, 6])
        self.qr = np.radians([140, 70, 45, 150, 10, 0])
        self.qz = np.radians([0, 0, 0, 0, 0, 0])
        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

    @property
    def MYCONFIG(self):
        return self._MYCONFIG


if __name__ == "__main__":
    from pathlib import Path
    PROJECT_ROOT_PATH = Path(__file__).absolute().parent.parent
    robot_arm_config_file = PROJECT_ROOT_PATH /  "config/robot_mdh_parameters.yaml"
    
    mirobot = Mirobot(robot_arm_config_file)
    print(mirobot)

    # 机械臂正运动解
    q1 = radians(0)
    q2 = radians(20)
    q3 = radians(0)
    q4 = radians(0)
    q5 = radians(0)
    q6 = radians(0)
    print("机械臂关节角度 = ", [round(degrees(i), 2) for i in [q1, q2, q3, q4, q5, q6]])
    arm_pose_degree = np.array([q1, q2, q3, q4, q5, q6])
    translation_vector = mirobot.fkine(arm_pose_degree)

    print("机械臂正解结果")
    print(translation_vector.printline(), '\n')
    x, y, z = translation_vector.t  # 平移向量
    print("x = ", round(x, 3))
    print("y = ", round(y, 3))
    print("z = ", round(z, 3))
    print('')
    Rz, Ry, Rx = translation_vector.rpy(unit='deg')  # 旋转角
    print("r = ", round(Rz, 3))
    print("p = ", round(Ry, 3))
    print("y = ", round(Rx, 3))
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
    specified_data = list(map(lambda d: round(degrees(d), 1), [q1, q2, q3, q4, q5, q6]))
    occurrences = rs_ik.count(specified_data)
    print("Occurrences:", occurrences)

    # 机械臂画图
    mirobot.teach(mirobot.qz, block=True)
    
