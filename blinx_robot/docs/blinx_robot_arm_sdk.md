# 比邻星机械臂 Python 接口文档

[TOC]

## 1.连接机械臂

```python
from blx_robot import *
robot=BlxRobot(ip, port)
```

| 函数名称： | BlxRobot(ip,pot)                       |
| ---------- | -------------------------------------- |
| 功能描述   | 机械臂控制类                           |
| 参数说明   | ip：机械臂IP地址<br>port：机械臂端口号 |

## 2.机械臂自动回零运动

| 函数名称: | set_joint_Auto_zero()    |
| --------- | ------------------------ |
| 功能描述: | 机械臂自动回零运动       |
| 参数说明: | 无                       |
| 返回值:   | 成功:true     失败:false |

**python示例代码**

```python
# 机械臂自动回零
robot.set_joint_Auto_zero()
```

## 3.设置机械臂单个轴角度运动控制

| 函数名称: | set_joint_angle(axle,angle, speed)                           |
| --------- | ------------------------------------------------------------ |
| 功能描述: | 机械臂单关节角度运动控制                                     |
| 参数说明: | axle (int): 机械臂1-6轴，范围为【1-6】<br>angle (float): 角度值<br>第一轴范围【-165°—165°】<br>第二轴范围【-90°—90°】<br>第三轴范围【-60°—90°】<br>第四轴范围【-150°—170°】<br>第五轴范围【-30°—210°】<br>第六轴范围【-180°—180°】<br>speed (int): 速度百分比，范围为【0-100】 |
| 返回值:   | {'return': 'set_joint_angle_speed', 'data':true} <br>成功:true     失败:false |

**python示例代码**

```python
# 设置第一轴角度为130度，速度百分比为20
robot.set_joint_angle(1,130,20)
```

## 4.设置机械臂单个轴坐标运动控制

| 函数名称: | set_coordinate_axle(axle,value,speed)                        |
| --------- | ------------------------------------------------------------ |
| 功能描述: | 机械臂单坐标运动控制                                         |
| 参数说明: | axle (int): 机械臂X，Y，Z，RX，RY，RZ轴，范围为【1-6】<br>value (float): 坐标值<br>speed (int): 速度百分比，范围为【0-100】 |
| 返回值:   | {'return': 'set_joint_angle_speed', 'data':true} <br>成功:true     失败:false |

**python示例代码**

```python
# 设置X轴坐标值为200，速度百分比为20
robot.set_joint_angle(1,200,20)
```

## 5.设置机械臂多关节角度运动控制

| 函数名称: | set_joint_angle_all_speed(axle1,axle2,axle3,axle4,axle5,axle6, speed) |
| --------- | ------------------------------------------------------------ |
| 功能描述: | 机械臂多关节角度运动控制                                     |
| 参数说明: | axle1-axle6  (float): 机械臂1-6轴角度值<br>第一轴范围【-165°—165°】<br>第二轴范围【-90°—90°】<br>第三轴范围【-60°—90°】<br>第四轴范围【-150°—170°】<br>第五轴范围【-30°—210°】<br>第六轴范围【-180°—180°】<br>speed (int): 速度百分比，范围为【0-100】 |
| 返回值:   | {'return': 'set_joint_angle_all_speed', 'data':true} <br>成功:true     失败:false |

**python示例代码**

```python
# 设置第一轴到第六轴角度值，速度百分比为20
robot.set_joint_angle_all_speed(140,60,35,140,0,-10,20)
```

## 6.设置机械臂坐标运动控制

| 函数名称: | set_coordinate_axle_all_speed(axle1,axle2,axle3,axle4,axle5,axle6,speed) |
| --------- | ------------------------------------------------------------ |
| 功能描述: | 机械臂坐标运动控制                                           |
| 参数说明: | axle1-axle6  (float): 机械臂X，Y，Z，RX，RY，RZ轴坐标值<br>speed (int): 速度百分比，范围为【0-100】 |
| 返回值:   | {'return': 'set_joint_angle_all_speed', 'data':true} <br>成功:true     失败:false |

**python示例代码**

```python
# 设置机械臂X，Y，Z，RX，RY，RZ坐标值，速度百分比为20
robot.set_coordinate_axle_all_speed(40,40,40,40,40,40,20)
```

## 7.查询机械臂关节角度信息

| 函数名称: | get_joint_angle_all()                                        |
| --------- | ------------------------------------------------------------ |
| 功能描述: | 查询机械臂关节角度信息                                       |
| 参数说明: | 无                                                           |
| 返回值:   | {'return': 'get_joint_angle_all', 'data': [150, 70, 45, 150, 10, 0]}<br>成功：机械臂当前第一轴到第六轴角度值   失败:false |

**python示例代码**

```python
# 查询机械臂关节角度信息
robot.get_joint_angle_all()
```

## 8.机械臂IO控制

| 函数名称: | set_robot_io_interface(IO,Bourg)                             |
| --------- | ------------------------------------------------------------ |
| 功能描述: | 机械臂IO控制                                                 |
| 参数说明: | IO (int): 机械臂的IO口，范围为 【0-4】<br>Bourg (bool): IO设备开关，True or False |
| 返回值:   | {'return': 'set_robot_io_interface', 'data':true} <br>成功:true     失败:false |

**python示例代码**

```python
# 机械臂打开编号1的IO口
robot.set_robot_io_interface(1,True)
```

## 9.正解

| 函数名称: | get_positive_solution(axle1, axle2, axle3, axle4, axle5, axle6) |
| --------- | ------------------------------------------------------------ |
| 功能描述: | 正解                                                         |
| 参数说明: | axle1-axle6  (float): 机械臂1-6轴角度值<br>第一轴范围【-165°—165°】<br>第二轴范围【-90°—90°】<br>第三轴范围【-60°—90°】<br>第四轴范围【-150°—170°】<br>第五轴范围【-30°—210°】<br>第六轴范围【-180°—180°】 |
| 返回值:   | {'return': 'get_positive_solution', 'data':[0，0，0，0，0，0]} <br>成功：机械臂X，Y，Z，RX，RY，RZ坐标值   失败:false |

**python示例代码**

```python
# 正解
robot.get_positive_solution(150, 70, 45, 150, 10, 0)
```

## 10.逆解

| 函数名称:  | get_inverse_kinematics(axle1, axle2, axle3, axle4, axle5, axle6) |
| ---------- | ------------------------------------------------------------ |
| 功能描述:  | 逆解                                                         |
| 参数说明:: | axle1-axle6  (float): 机械臂X，Y，Z，RX，RY，RZ轴坐标值      |
| 返回值:    | {'return': 'get_inverse_kinematics', 'data':[0，0，0，0，0，0]} <br>成功：机械臂当前第一轴到第六轴角度值   失败:false |

**python示例代码**

```python
# 逆解
robot.get_inverse_kinematics(0，0，0，0，0，0)
```

## 11.温度查询

| 函数名称:  | get_temperature()                                            |
| ---------- | ------------------------------------------------------------ |
| 功能描述:  | 机械臂温度查询                                               |
| 参数说明:: | 无                                                           |
| 返回值:    | {'return': 'get_temperature', 'data':[0]} <br>成功：机械臂当前温度值   失败:false |

**python示例代码**

```python
# 温度查询
robot.get_temperature()
```

## 12.io输入查询

| 函数名称:  | get_output()                                                 |
| ---------- | ------------------------------------------------------------ |
| 功能描述:  | io输入获取                                                   |
| 参数说明:: | 无                                                           |
| 返回值:    | {'return': 'get_output', 'data':[0]} <br>成功：机械臂当前io输入   失败:false |

**python示例代码**

```python
# 温度查询
robot.get_output()
```

## 13.电压查询

| 函数名称:  | get_current_voltage()                                        |
| ---------- | ------------------------------------------------------------ |
| 功能描述:  | 获取机械臂当前电流电压                                       |
| 参数说明:: | 无                                                           |
| 返回值:    | {'return': 'get_current_voltage', 'data':[0]} <br>成功：机械臂当前电流电压   失败:false |

**python示例代码**

```python
# 温度查询
robot.get_current_voltage()
```

## 14.机械臂配置有线网 IP 地址 

| 函数名称:  | set_NetIP(IP)                                                |
| ---------- | ------------------------------------------------------------ |
| 功能描述:  | 配置有线网卡IP地址                                         |
| 参数说明:: | 配置有线网口IP地址                                      |
| 返回值:    | {'return': 'set_NetIP', 'data':true} <br>成功：true   失败:false |

**python示例代码**

```python
# 温度查询
robot.set_NetIP("192.168.5.111")
```













