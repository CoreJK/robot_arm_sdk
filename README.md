# 比邻星六轴机械臂 SDK

## 目录

- [比邻星六轴机械臂 SDK](#比邻星六轴机械臂-sdk)
  - [目录](#目录)
  - [项目简介 ](#项目简介-)
  - [SDK 设计框图](#sdk-设计框图)
  - [开发 ](#开发-)
    - [机械臂 MDH 参数](#机械臂-mdh-参数)
    - [安装](#安装)
  - [示例代码 ](#示例代码-)

## 项目简介 <a name = "about"></a>

基于 python3 的比邻星六轴机械臂，用于二次开发的 SDK

## SDK 设计框图

![SDK 通讯设计](https://s2.loli.net/2024/05/17/2JANMPSqYWh46C1.png)

机械臂建立连接后，线程池启动：

1. 启动【发送线程】；
2. 启动【接收线程】；
3. 调用【普通 API 方法】启动对应命令的【分流线程】；
4. 【分流线程】开始轮询【命令执行结果队列】；
5. 【普通 API 方法】将需要执行的命令，放入【待发送命令队列】；
6. 【发送线程】从【待发送命令队列】取出一条命令；
7. 【发送线程】发送命令给【机械臂】；
8. 【接收线程】收到【机械臂】返回的命令执行结果；
9. 【接收线程】将命令放入【命令执行结果队列】；
10. 【分流线程】从队列中获取返回的命令执行结果，并找到需要的结果消息；
11. 【普通 API 方法】拿到返回的数据；
12. 【普通 API 方法】返回执行结果；
13. 【普通 API 方法】记录命令的执行情况；

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
| 4 | -pi / 2 | 0 | 223 | 0       |
| 5 | pi / 2  | 0 | 0      | pi/2    |
| 6 | pi / 2  | 0 | -108.79 | 0       |

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

**在发布页面, 下载最新分支版本, 发布的 whl 安装包**
通过 pip 安装即可

```
pip install blinx_robots-4.3.0-py3-none-any.whl
```

卸载

```
pip uninstall blinx_robots
```

接下来, 在自己的代码中, 导入模块开始使用
下面提供了实列代码

## 示例代码 <a name = "usage"></a>

导入模块

```python
import time
import json

from loguru import logger

from blinx_robots.robot_arm_interface import BlxRobotArm
from blinx_robots.robot_arm_communication import SocketCommunication
```

实例化机械臂对象

```python
# 连接机械臂
host = "192.168.10.111"
port = 1234
socket_communication = SocketCommunication(host, port)
robot = BlxRobotArm(socket_communication)
```

控制机械臂

```python
# 机械臂通讯连接
logger.warning("\n1: 测试机械臂通讯连接")
robot.start_communication()

# 获取机械臂的命令执行模式
logger.warning("\n2: 测试机械臂命令执行模式")
robot_cmd_model = json.loads(robot.get_robot_cmd_model()).get('data') 
logger.info(f"机械臂的命令执行模式: {robot_cmd_model}")

# 设置机械臂的命令模式
logger.warning("\n3: 测试机械臂命令执行模式设置")
# robot.set_robot_cmd_mode("INT")
# time.sleep(1)
robot.set_robot_cmd_mode("SEQ")
time.sleep(1)

# 机械臂初始化，将机械臂关节角度归零
logger.warning("\n4: 测试机械臂初始化")
robot.set_robot_arm_init()
time.sleep(12)

# 获取机械臂关节角度
logger.warning("\n5: 测试机械臂关节角度")
robot.get_joint_degree_all()
time.sleep(1)

# 设置机械臂单个关节角度
logger.warning("\n6: 测试机械臂单个关节角度设置")
robot.set_joint_degree_by_number(1, 50, 90)

# 获取机械臂所有当前关节角度
logger.warning("\n7: 测试机械臂所有关节角度设置")
joint_degree = robot.get_joint_degree_all().get('data')
logger.info(f"机械臂所有关节角度: {joint_degree}")
time.sleep(1)

# 机械臂紧急停止
logger.warning("\n8: 测试机械臂紧急停止")
robot.set_robot_arm_emergency_stop()
time.sleep(2)

# 恢复机械臂状态
logger.warning("\n9: 测试机械臂急停后的状态恢复上电")
robot.set_robot_arm_init()
time.sleep(2)
logger.warning("\n10: 测试机械臂急停后的状态恢复")
robot.set_robot_arm_init()
time.sleep(12)

# 设置机械臂末端工具控制
logger.warning("\n11: 测试机械臂末端工具控制使能")
robot.set_robot_end_tool(1, True)  # 控制气泵打开
time.sleep(2)
logger.warning("\n12: 测试机械臂末端工具控制掉使能")
robot.set_robot_end_tool(1, False)  # 控制气泵关闭
time.sleep(2)

# 设置机械臂所有关节角度协同运动
logger.warning("\n13: 测试机械臂所有关节角度协同运动")
robot.set_joint_degree_synchronize(10, 10, 10, 10, 10, 10, speed_percentage=50)
time.sleep(2)

# 通过末端工具坐标与姿态，控制机械臂关节运动
logger.warning("\n14: 测试通过末端工具坐标与姿态，控制机械臂关节运动")
robot.set_joint_degree_by_coordinate(0.287, 0.0, 0.269, 0.0, -0.0, 0.0, speed_percentage=50)
time.sleep(5)

# 机械臂回零
logger.warning("\n15: 测试机械臂回零")
robot.set_robot_arm_home()
time.sleep(2)

# 获取机械臂正解
logger.warning("\n16: 测试获取机械臂当前角度的, 正解")
robot.get_positive_solution(current_pose=True)
logger.warning("\n17: 测试获取机械臂单独计算正解")
robot.get_positive_solution(20, 0, 0, 0, 0, 0, current_pose=False)

# 获取机械臂逆解
logger.warning("\n18: 测试获取机械臂当前角度的, 逆解")
robot.get_inverse_solution(current_pose=True)
logger.warning("\n19: 测试获取机械臂单独计算逆解")
robot.get_inverse_solution(0.23, 0.084, 0.269, 20.0, -0.0, -0.0, current_pose=False)

# 顺序执行模式中, 使用延时命令
logger.warning("\n20: 测试机械臂顺序执行模式中, 使用延时命令")
robot.set_joint_degree_synchronize(10, 10, 10, 10, 10, 10, speed_percentage=50)
robot.set_time_delay(3000)
robot.set_robot_end_tool(1, True)
robot.set_time_delay(3000)
robot.set_robot_end_tool(1, False)
robot.set_time_delay(3000)
robot.set_joint_degree_synchronize(20, 20, 20, 20, 20, 20, speed_percentage=50)
robot.set_time_delay(3000)
robot.set_robot_arm_home()
time.sleep(3)

# 机械臂通讯关闭
logger.warning("\n21: 测试机械臂通讯关闭")
robot.end_communication()
```