# 比邻星六轴机械臂 SDK

## 目录

- [比邻星六轴机械臂 SDK](#比邻星六轴机械臂-sdk)
  - [目录](#目录)
  - [项目简介 ](#项目简介-)
  - [开发 ](#开发-)
    - [机械臂 MDH 参数](#机械臂-mdh-参数)
    - [安装](#安装)
  - [示例代码 ](#示例代码-)

## 项目简介 <a name = "about"></a>

基于 python3 的比邻星六轴机械臂，用于二次开发的 SDK

## 开发 <a name = "getting_started"></a>

**从内网拉取 develop 分支代码**

> 如果发现 BUG 请基于 develop 分支，开启新的分支
> 在新分支修复问题后，合并到 develop 后提交，谢谢！

```shell
git clone -b develop http://192.168.10.69:10880/Education_Department/robot_arm_sdk.git
cd robot_arm_sdk
```

配置虚拟环境

```shell
python -m venv venv

# windows
venv\Scripts\activate.bat

# linux
source venv/bin/activate

# 配置依赖环境
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 机械臂 MDH 参数

MDH 参数

| 关节 | alpha   | a | d      | theta   |
| ---- |---------| -- |--------|---------|
| 1 | 0       | 0 | 153.50  | 0       |
| 2 | -pi / 2 | 24 | 0      | -pi / 2 |
| 3 | 0       | 160.72 | 0      | 0       |
| 4 | -pi / 2 | 0 | 220.50 | 0       |
| 5 | pi / 2  | 0 | 0      | pi/2    |
| 6 | pi / 2  | 0 | -45 | 0       |

机械臂电机方向与角度范围

> 先将屏幕面向操作者，将机械臂回零，再确定电机的角度正负值，以及对应的控制方向
>
> 需要与正逆解模型的角度方向一致

| 电机编号 | 方向   | 负值（度） | 正值(度) | 方向   | 备注 |
| -------- | ------ | ---------- | -------- | ------ | ---- |
| 1        | 顺时针 | -140       | +140     | 逆时针 | 俯视 |
| 2        | 顺时针 | -70        | +70      | 逆时针 | 左视 |
| 3        | 顺时针 | -60        | +45      | 逆时针 | 左视 |
| 4        | 逆时针 | -150       | +150     | 顺时针 | 正视 |
| 5        | 顺时针 | -180       | +10      | 逆时针 | 左视 |
| 6        | 顺时针 | -180       | +180     | 逆时针 | 俯视 |

### 安装

A step by step series of examples that tell you how to get a development env running.

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo.

## 示例代码 <a name = "usage"></a>

导入模块

```python
from blinx_robot import BlxRobotArm
from pathlib import Path
```

实例化机械臂对象

```python
# 读取机械臂 MDH 配置文件
PROJECT_ROOT_PATH = Path(__file__).absolute().parent.parent
robot_arm_config_file = PROJECT_ROOT_PATH / "config/robot_mdh_parameters.yaml"

# 连接机械臂
host = "192.168.10.234"
port = 1234
robot = BlxRobotArm(host, port, robot_arm_config_file)
```

控制机械臂

```python
# 机械臂初始化，将机械臂关节角度归零
print(robot.set_robot_arm_init())

# 获取机械臂关节角度
print(robot.get_joint_degree_all())

# 设置指定的机械臂关节角度
print(robot.set_joint_degree_by_number(1, 50, 50))

# 设置机械臂所有关节角度同时运动
print(robot.set_joint_degree_synchronize(20, 0, 0, 0, 0, 0, speed_percentage=50))

# 获取机械臂正解
print(robot.get_positive_solution(20, 0, 0, 0, 0, 0, current_pose=False))  # 传入自定义关节角度值获取正解
print(robot.get_positive_solution(current_pose=True))  # 根据机械臂当前关节角度获取正解

# 获取机械臂逆解
print(robot.get_inverse_solution(0.23, 0.084, 0.269, 20.0, -0.0, -0.0, current_pose=False))  # 传入自定义末端位姿获取逆解
print(robot.get_inverse_solution(current_pose=True))  # 根据机械臂当前末端位姿获取逆解

# 根据坐标系位置和姿态控制机械臂运动
print(robot.set_joint_degree_by_coordinate(0.23, 0.084, 0.269, 20.0, -0.0, -0.0, speed_percentage=50))

# 控制IO口
print(robot.set_robot_io_interface(0, True))  # 打开IO口
print(robot.set_robot_io_interface(0, False))  # 关闭IO口
```