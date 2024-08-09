# 比邻星机械臂 Python 接口文档

[TOC]

## 1.安装需要的模块

**在发布页面, 下载最新分支版本, 发布的 whl 安装包**

通过 pip 安装即可（版本会更新，需安装最新的版本）

```
pip install blinx_robots-<版本号>-py3-none-any.whl
```

举例

```python
pip install blinx_robots-4.3.0-py3-none-any.whl
```

卸载

```python
pip uninstall blinx_robots
```

接下来, 在自己的代码中, 导入模块开始使用
下面提供了实列代码

## 2.连接机械臂

```python
import json
from blinx_robots.robot_arm_interface import BlxRobotArm
from blinx_robots.robot_arm_communication import SocketCommunication
socket_communication = SocketCommunication(host, port)
robot = BlxRobotArm(socket_communication)
robot.start_communication()
```

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >SocketCommunication(ip, port)</th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂连接类</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >ip：机械臂IP地址<br>port：机械臂端口号</td>
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
    <td >机械臂初始化，将机械臂关节角度归零</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >无</td>
  </tr>
  <tr>
    <td style="width: 100px;">返回值</td>
    <td >成功：{"command": "set_joint_initialize", "status": true}<br>失败：{"command": "set_joint_initialize", "status": false}</td>
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
    <td >成功：{"command": "set_robot_arm_home", "status": true}<br>失败：{"command": "set_robot_arm_home", "status": false}</td>
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
    <td >  "INT"：立即执行指令， 适用场景： 立即执行控制，新指令会覆盖正在执行的指令得到立即响应；但是如果一次性发送一系列指令的话则效果会是只执行最后一条；适合场景例如动作同步。<br>  "SEQ"： 顺序执行指令，适用场景： 一次性发送几个关键点位姿，等待依次执行，可以确保关键点到达；但是由于关键点之间存在减速到0的过程所以存在一定停顿；适合场景例如视觉抓取、码垛等应用。</td>
  </tr>
  <tr>
    <td style="width: 100px;">返回值</td>
    <td >成功：{"command": "set_robot_mode", "status": true}<br>失败：{"command": "set_robot_mode", "status": false}</td>
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
    <th >get_robot_cmd_mode() </th>
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
    <td >"INT"：立即执行指令<br> "SEQ"： 顺序执行指令</td>
  </tr>
</table>


**python示例代码**

```python
# 获取机械臂的命令执行模式
robot_cmd_model = json.loads(robot.get_robot_cmd_mode()).get('data')
print(f"机械臂的命令执行模式: {robot_cmd_model}")
```

## 7.设置机械臂单个轴角度运动控制

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_joint_degree_by_number(joint_number, speed_percentage, joint_degree) </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂单关节角度运动控制</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td > joint_number (int): 机械臂1-6轴，范围为【1-6】<br>speed_percentage (int): 速度百分比，范围为【0-100】<br>joint_degree (float): 角度值<br>第一轴范围【-140°—140°】<br>第二轴范围【-70°—70°】<br>第三轴范围【-60°—45°】<br>第四轴范围【-150°—150°】<br>第五轴范围【-180°—10°】<br>第六轴范围【-180°—180°】</td>
  </tr>
  <tr>
    <td style="width: 100px;">返回值</td>
     <td >成功：{"command": "set_joint_angle", "status": true}<br>失败：{"command": "set_joint_angle", "status": false}</td>
  </tr>
</table>


**python示例代码**

```python
# 设置第一轴角度为90度，速度百分比为50
robot.set_joint_degree_by_number(1, 50, 90)
```

## 8.设置机械臂所有关节角度协同运动

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_joint_degree_synchronize(*args, speed_percentage)</th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂所有关节角度协同运动</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td > *args  (float): 机械臂1-6轴角度值<br>第一轴范围【-140°—140°】<br>第二轴范围【-70°—70°】<br>第三轴范围【-60°—45°】<br>第四轴范围【-150°—150°】<br>第五轴范围【-180°—10°】<br>第六轴范围【-180°—180°】<br>speed_percentage(int): 速度百分比，范围为【0-100】</td>
  </tr>
  <tr>
    <td style="width: 100px;">返回值</td>
  <td >成功：{"command": "set_joint_angle_all_time", "status": true}<br>失败：{"command": "set_joint_angle_all_time", "status": false}</td>
  </tr>
</table>

**python示例代码**

```python
# 设置第一轴到第六轴角度值都为10，速度百分比为50
robot.set_joint_degree_synchronize(10, 10, 10, 10, 10, 10, speed_percentage=50)
```

## 9.设置机械臂坐标运动控制

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_robot_arm_coordinate(*args, speed_percentage)  </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂坐标运动控制</td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td > *args(float): 机械臂X，Y，Z，RX，RY，RZ轴坐标值<br>speed_percentage(int): 速度百分比，范围为【0-100】</td>
  </tr>
  <tr>
    <td style="width: 100px;">返回值</td>
  <td >成功：{"command": "set_robot_arm_coordinate", "status": true}<br>失败：{"command": "set_robot_arm_coordinate", "status": false}</td>
  </tr>
</table>


**python示例代码**

```python
# 设置机械臂X，Y，Z，RX，RY，RZ坐标值，速度百分比为50
robot.set_robot_arm_coordinate(0.287, 0.0, 0.269, 0.0, -0.0, 0.0,speed_percentage=50)
```

## 10.查询机械臂所有当前关节角度

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >get_joint_degree_all()</th>
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
     <td >成功：获得当前所有关节角度字典{'return': 'get_joint_angle_all', 'data': [0, 15.358125, -16.7925, 0, 0, 0]}<br>失败：获得上一次所有关节角度字典{'return': 'get_joint_angle_all', 'data': [0, 12.364688, 0, 0, 0, 0]}</td>
  </tr>
</table>

**python示例代码**

```python
# 查询机械臂所有当前关节角度
joint_degree = robot.get_joint_degree_all().get('data')
print(f"机械臂所有关节角度: {joint_degree}")
```

## 11.机械臂外部IO控制

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_robot_io_status(io, status) </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂外部IO控制  </td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >io(int): 机械臂的外部IO口，范围为 【0-4】<br>status(bool): 设备开关状态，True or False</td>
  </tr>
  <tr>
    <td style="width: 100px;">返回值</td>
   <td >成功：{"command": "set_io_status", "status": true}<br>失败：{"command": "set_io_status", "status": false}</td>
  </tr>
</table>


**python示例代码**

```python
# 机械臂打开编号1的外部IO口
robot.set_robot_io_status(1, True)
```

## 12.设置机械臂末端工具控制

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_robot_end_tool(io, status) </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >机械臂末端工具控制  </td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >io (int): 机械臂末端 IO口，范围为 【0-3】<br>status (bool): IO设备开关，True or False</td>
  </tr>
  <tr>
    <td style="width: 100px;">返回值</td>
   <td >成功：{"command": "set_end_tool", "status": true}<br>失败：{"command": "set_end_tool", "status": false}</td>
  </tr>
</table>


**python示例代码**

```python
# 机械臂打开编号1的末端IO口
robot.set_robot_end_tool(1, True)
```

## 13.获取机械臂当前角度的正解值

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >get_robot_coordinate() </th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >获取机械臂当前角度的正解值 </td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >无</td>
  </tr>
  <tr>
    <td style="width: 100px;">返回值</td>
    <td >成功：{"command": "get_positive_solution", "data": [244.5, 0, 268.220001, 180.000015, 0, 0]}<br>机械臂X，Y，Z，RX，RY，RZ坐标值   <br>失败：{"command": "get_positive_solution", "data": []}</td>
  </tr>
</table>

**python示例代码**

```python
# 获取机械臂当前角度的正解值
robot.get_robot_coordinate()
```

## 14.延时命令（顺序执行指令使用）

<table>
  <tr>
    <th style="width: 100px;">函数名称：</th>
    <th >set_time_delay(delay_time: int)</th>
  </tr>
  <tr>
    <td style="width: 100px;">功能描述  </td>
    <td >执行过程中延时 </td>
  </tr>
  <tr>
    <td style="width: 100px;">参数说明</td>
    <td >millisecond：毫秒，范围 0 ~ 3000</td>
  </tr>
  <tr>
    <td style="width: 100px;">返回值</td>
     <td >成功：{"command": "set_time_delay", "status": true}<br>失败：{"command": "set_time_delay", "status": false}</td>
  </tr>
</table>


**python示例代码**

```python
if robot_cmd_model == "SEQ":
    # 顺序执行指令中, 使用延时命令
    robot.set_joint_degree_synchronize(10, 10, 10, 10, 10, 10, speed_percentage=50)
    robot.set_time_delay(3000)
    robot.set_robot_end_tool(1, True)
    robot.set_time_delay(3000)
    robot.set_robot_end_tool(1, False)
    robot.set_time_delay(3000)
    robot.set_joint_degree_synchronize(20, 20, 20, 20, 20, 20, speed_percentage=50)
    robot.set_time_delay(3000)
    robot.set_robot_arm_home()
```

## 15.机械臂紧急停止

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
<td >成功：{"command": "set_joint_emergency_stop", "status": true}<br>无失败返回值</td>
**python示例代码**

```python
# 机械臂紧急停止
robot.set_robot_arm_emergency_stop()
```

## 16.机械臂通讯关闭

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



