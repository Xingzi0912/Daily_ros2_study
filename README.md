# ROS2 学习工作空间

> 个人 ROS2 学习项目，基于 ROS2 Humble，涵盖 URDF 建模、节点编程、话题通信、仿真环境等内容。

---

## 📁 工作空间结构

```
ros2_ws/
├── src/
│   ├── interface/          # 自定义消息接口
│   ├── mybot_description/  # 机器人 URDF/Xacro 模型与显示
│   ├── my_cpp_pkg/         # C++ 示例节点
│   ├── my_py_pkg/          # Python 示例节点
│   └── wpr_simulation2/    # 仿真环境与综合 demo
├── build/                  # 编译产物
├── install/                # 安装产物
└── log/                    # 编译日志
```

---

## 📦 功能包说明

### 1. `interface` — 自定义消息接口

- 定义了 `Novel.msg` 消息类型
- 包含字段：`string content`、`sensor_msgs/Image image`
- 被 `my_py_pkg` 中的节点使用

### 2. `mybot_description` — 机器人模型描述

#### URDF/Xacro 模型

| 文件 | 说明 |
|------|------|
| `urdf/first_robot.xacro` | 初代机器人模型（单 base + 两个 IMU） |
| `urdf/first_robot.urdf` | 初代模型展开后的 URDF |
| `urdf/fishbot/fishbot.urdf.xacro` | **FishBot 主模型**（模块化传感器设计） |
| `urdf/fishbot/base.urdf.xacro` | FishBot 底盘 |
| `urdf/fishbot/sensor/imu.urdf.xacro` | IMU 传感器宏 |
| `urdf/fishbot/sensor/camera.urdf.xacro` | 摄像头传感器宏 |
| `urdf/fishbot/sensor/laser.urdf.xacro` | 激光雷达传感器宏（含支撑杆、碰撞检测） |
| `urdf/fishbot/actuator/wheel.xacro` | 驱动轮宏（圆柱形，半径 0.032m，长度 4cm） |
| `urdf/fishbot/actuator/caster.xacro` | 万向轮宏（球形，半径 0.032m） |

#### FishBot 模型特点

- **模块化设计**：传感器通过 Xacro 宏独立定义，主模型统一调用
- **支撑杆结构**：激光雷达通过 `laser_support_link` 支撑杆固定，支撑杆位置由参数决定
- **执行器模块**：驱动轮（`wheel_xacro`）和万向轮（`caster_xacro`）独立封装，支持差速驱动
- **碰撞检测**：所有 link 均包含 `<collision>` 标签，兼容 Gazebo 物理仿真
- **惯性参数**：所有 link 均包含 `<inertial>` 标签，兼容 Gazebo 仿真

#### 启动文件

```bash
# 显示机器人模型（RViz）
ros2 launch mybot_description dispaly_robot.launch.py

# 启动 Gazebo 仿真（自动加载 FishBot）
ros2 launch mybot_description gazebo_sim.launch.py
```

### 3. `my_cpp_pkg` — C++ 节点示例

| 文件 | 说明 |
|------|------|
| `src/chao_node.cpp` | 基础节点示例，演示 ROS2 C++ 节点创建 |

**节点类**：`SingleDogNode`，继承自 `rclcpp::Node`

### 4. `my_py_pkg` — Python 节点示例

| 文件 | 说明 |
|------|------|
| `my_py_pkg/li4.py` | 话题发布/订阅综合示例 |

**功能**：
- 发布 `String` 消息到 `man_what_can_i_say` 话题（定时器 4s）
- 订阅 `UInt32` 消息从 `kobe_money` 话题
- 使用自定义消息 `interface/msg/Novel`

### 5. `wpr_simulation2` — 仿真综合包

基于 Gazebo 的机器人仿真环境，来自 [6-robot](http://www.6-robot.com)。

#### 核心功能

| 目录 | 内容 |
|------|------|
| `launch/` | SLAM、导航、物体生成、场景加载等启动文件 |
| `demo_cpp/` | 20+ C++ demo（话题、服务、参数、视觉、导航等） |
| `demo_launch/` | 多种格式的 launch 示例（Python/XML/YAML） |
| `demo_package/` | 对应的 package 运行配置 |
| `exercises/` | 练习代码与扩展功能 |
| `config/` | Nav2 参数、控制器配置 |
| `src/` | 仿真节点源码（键盘控制、物体抓取、人脸检测等） |

#### 常用启动命令

```bash
# 启动仿真世界
ros2 launch wpr_simulation2 world.launch.py

# SLAM 建图
ros2 launch wpr_simulation2 slam.launch.py

# 导航
ros2 launch wpr_simulation2 navigation.launch.py

# 机械臂控制
ros2 launch wpr_simulation2 demo_mani_ctrl.launch.py
```

---

## 🚀 快速开始

### 环境要求

- ROS2 Humble
- Ubuntu 22.04
- Gazebo（用于 wpr_simulation2）

### 编译工作空间

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

### 运行示例

```bash
# 显示 FishBot 模型
ros2 launch mybot_description dispaly_robot.launch.py

# 运行 C++ 节点
ros2 run my_cpp_pkg chao_node

# 运行 Python 节点
ros2 run my_py_pkg li4
```

---

## 📝 学习记录

| 日期 | 内容 |
|------|------|
| 5月3日-5日 | ROS2 基础节点、话题通信 |
| 5月13日 | 自定义消息接口 |
| 5月17日 | URDF/Xacro 建模、FishBot 传感器模块化设计 |
| 5月18日 | 执行器建模（驱动轮/万向轮 Xacro 宏）、碰撞标签、Gazebo 仿真启动文件 |

---

## 🔗 相关链接

- [ROS2 Humble 官方文档](https://docs.ros.org/en/humble/)
- [6-robot 官网](http://www.6-robot.com)
