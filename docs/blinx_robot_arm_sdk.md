# 比邻星机械臂 Python 接口文档

[TOC]

## 1.安装需要的模块

**在发布页面, 下载最新分支版本, 发布的 whl 安装包**
通过 pip 安装即可

```python
pip install blinx_robots-4.3.1-py3-none-any.whl -i https://pypi.tuna.tsinghua.edu.cn/simple
```

卸载

```python
pip uninstall blinx_robots
```

接下来, 在自己的代码中, 导入模块开始使用
下面提供了实列代码

## 2.连接机械臂

```python
import time
import json
from loguru import logger
from blinx_robots.robot_arm_interface import BlxRobotArm
from blinx_robots.robot_arm_communication import SocketCommunication
socket_communication = SocketCommunication(host, port)
robot = BlxRobotArm(socket_communication)
robot.start_communication()
```

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >SocketCommunication(ip,port)</th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂连接类</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >ip：机械臂IP地址<brport：机械臂端口号</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >无</td>
  </tr>

</table>

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >BlxRobotArm(socket_communication)</th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂控制类</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >socket_communication：串口连接对象</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >无</td>
  </tr>

</table>

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >start_communication()</th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >开启通讯</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >无</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >无</td>
  </tr>

</table>

## 3.机械臂初始化

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_robot_arm_init() </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >让电机使能，找到每个电机对应的初始化位置</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >无</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >无</td>
  </tr>

</table>

**python示例代码**

```python
# 机械臂自动回零
robot.set_robot_arm_init()
```

## 4.机械臂自动回零运动

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_robot_arm_home() </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂自动回零运动</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >无</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >成功:true     失败:false</td>
  </tr>

</table>

**python示例代码**

```python
# 机械臂自动回零
robot.set_robot_arm_home()
```

## 5.设置机械臂的命令模式

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_robot_cmd_mode(mode) </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >设置机械臂的命令模式</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >  "INT"：实时指令模式， 适用场景： 用于实时控制，新指令会覆盖正在执行的指令得到立即响应；但是如果一次性发送一系列指令的话则效果会是只执行最后一条；适合场景例如动作同步。<br>  "SEQ"： 顺序指令模式，适用场景： 一次性发送几个关键点位姿，等待依次执行，可以确保关键点到达；但是由于关键点之间存在减速到0的过程所以存在一定停顿；适合场景例如视觉抓取、码垛等应用。</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >无</td>
  </tr>

</table>

**python示例代码**

```python
# 设置机械臂的命令模式"INT"
robot.set_robot_cmd_mode("INT")
# 设置机械臂的命令模式"SEQ"
robot.set_robot_cmd_mode("SEQ")
```

## 6.获取机械臂的命令执行模式

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >get_robot_cmd_model() </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >获取机械臂的命令执行模式</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td > 无</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >"INT"：实时指令模式<br> "SEQ"： 顺序指令模式</td>
  </tr>

</table>

**python示例代码**

```python
# 获取机械臂的命令执行模式
robot_cmd_model = json.loads(robot.get_robot_cmd_model()).get('data')
logger.info(f"机械臂的命令执行模式: {robot_cmd_model}")
```

## 7.设置机械臂单个轴角度运动控制

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_joint_degree_by_number(axle,speed,angle) </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂单关节角度运动控制</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td > axle (int): 机械臂1-6轴，范围为【1-6】<br>speed (int): 速度百分比，范围为【0-100】<br>angle (float): 角度值<br>第一轴范围【-140°—140°】<br>第二轴范围【-70°—70°】<br>第三轴范围【-60°—45°】<br>第四轴范围【-150°—150°】<br>第五轴范围【-180°—10°】<br>第六轴范围【-180°—180°】</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >{"return":"move_in_place","data":"true"} <br>成功:true     失败:false</td>
  </tr>

</table>

**python示例代码**

```python
# 设置第一轴角度为90度，速度百分比为50
print(robot.set_joint_degree_by_number(1, 50, 90))
```

## 8.设置机械臂所有关节角度协同运动

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_joint_degree_synchronize(axle1,axle2,axle3,axle4,axle5,axle6, <br>speed_percentage)</th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂所有关节角度协同运动</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td > axle1-axle6  (float): 机械臂1-6轴角度值<br>第一轴范围【-140°—140°】<br>第二轴范围【-70°—70°】<br>第三轴范围【-60°—45°】<br>第四轴范围【-150°—150°】<br>第五轴范围【-180°—10°】<br>第六轴范围【-180°—180°】<br>speed_percentage(int): 速度百分比，范围为【0-100】</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >  {"return":"move_in_place","data":"true"} <br>成功:true     失败:false</td>
  </tr>

</table>

**python示例代码**

```python
# 设置第一轴到第六轴角度值都为10，速度百分比为50
print(robot.set_joint_degree_synchronize(10, 10, 10, 10, 10, 10, speed_percentage=50))
```

## 9.设置机械臂坐标运动控制

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_joint_degree_by_coordinate(axle1,axle2,axle3,axle4,axle5,axle6,<br>speed_percentage)  </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂坐标运动控制</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td > axle1-axle6  (float): 机械臂X，Y，Z，RX，RY，RZ轴坐标值<br>speed_percentage(int): 速度百分比，范围为【0-100】</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td > ？？？</td>
  </tr>

</table>

**python示例代码**

```python
# 设置机械臂X，Y，Z，RX，RY，RZ坐标值，速度百分比为50
robot.set_joint_degree_by_coordinate(0.287, 0.0, 0.269, 0.0, -0.0, 0.0, speed_percentage=50)
```

## 10.查询机械臂关节角度信息

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >get_joint_degree_all()   </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >查询机械臂关节角度信息</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >无</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >{'return': 'get_joint_angle_all', 'data': [0, 15.358125, -16.7925, 0, 1.431, 0]}<br>成功：机械臂当前第一轴到第六轴角度值   失败:false</td>
  </tr>

</table>

**python示例代码**

```python
# 查询机械臂关节角度信息
joint_degree = robot.get_joint_degree_all().get('data')
logger.info(f"机械臂所有关节角度: {joint_degree}")
```

## 11.机械臂IO控制

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_robot_end_tool(IO,Bourg) </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂IO控制  </td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >IO (int): 机械臂的IO口，范围为 【0-4】<br>Bourg (bool): IO设备开关，True or False</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >{"return":"set_end_tool","data":"true"} <br>成功:true     失败:false</td>
  </tr>

</table>

**python示例代码**

```python
# 机械臂打开编号1的IO口
robot.set_robot_end_tool(1, True) 
```

## 12.正解

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >get_positive_solution(axle1, axle2, axle3, axle4, axle5, axle6,current_pose) </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂正解 </td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >axle1-axle6  (float): 机械臂1-6轴角度值<br>第一轴范围【-165°—165°】<br>第二轴范围【-90°—90°】<br>第三轴范围【-60°—90°】<br>第四轴范围【-150°—170°】<br>第五轴范围【-30°—210°】<br>第六轴范围【-180°—180°】<br>current_pose: True：获取机械臂当前角度的正解，False：获取机械臂单独计算角度的正解</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >成功：{"command": "get_positive_solution", "data": [0.287, 0.0, 0.269, 0.0, -0.0, -0.0]} <br>机械臂X，Y，Z，RX，RY，RZ坐标值   <br>失败：{"command": "get_positive_solution", "data": []}</td>
  </tr>

</table>

**python示例代码**

```python
# 获取机械臂当前角度的正解
robot.get_positive_solution(current_pose=True)
# 获取机械臂单独计算角度的正解
robot.get_positive_solution(20, 0, 0, 0, 0, 0, current_pose=False)
```

## 13.逆解

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >get_inverse_solution(axle1, axle2, axle3, axle4, axle5, axle6,current_pose)</th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂逆解 </td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >axle1-axle6  (float): 机械臂X，Y，Z，RX，RY，RZ轴坐标值<br>current_pose: True：获取机械臂当前角度的逆解，False：获取机械臂单独计算角度的逆解</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >成功：{"command": "get_inverse_kinematics", "data": [-0.0, 15.359, -16.793, 0.0, 1.434, 0.0]}<br>机械臂当前第一轴到第六轴角度值   <br>失败：{"command": "get_inverse_kinematics", "data": []}</td>
  </tr>

</table>

**python示例代码**

```python
# 获取机械臂当前角度的逆解
robot.get_inverse_solution(current_pose=True)
# 获取机械臂单独计算角度的逆解
robot.get_inverse_solution(0.23, 0.084, 0.269, 20.0, -0.0, -0.0, current_pose=False)
```

## 14.机械臂紧急停止

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_robot_arm_emergency_stop()</th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂紧急停止 </td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >无</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >无</td>
  </tr>

</table>

**python示例代码**

```python
# 机械臂紧急停止
robot.set_robot_arm_emergency_stop()
```

## 15.机械臂通讯关闭

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >end_communication()</th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂通讯关闭 </td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >无</td>
  </tr>

  <tr>
    <td style="width: 100px;">返回值</td>
    <td >无</td>
  </tr>

</table>

**python示例代码**

```python
# 机械臂通讯关闭
robot.end_communication()
```



