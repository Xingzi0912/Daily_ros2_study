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

### `mybot_description` — 机器人模型描述

| 文件 | 说明 |
|------|------|
| `urdf/fishbot/fishbot.urdf.xacro` | FishBot 主模型（模块化传感器设计） |
| `urdf/fishbot/base.urdf.xacro` | 底盘 |
| `urdf/fishbot/sensor/*.xacro` | IMU、相机、激光雷达传感器宏 |
| `urdf/fishbot/actuator/*.xacro` | 驱动轮、万向轮宏 |
| `urdf/fishbot/plugins/*.xacro` | Gazebo 插件（控制、传感器） |
| `launch/gazebo_sim.launch.py` | Gazebo 仿真启动文件 |

### `wpr_simulation2` — 仿真综合包

来自 [6-robot](http://www.6-robot.com)，包含 SLAM、导航、机械臂控制等 demo。

---

## 🚀 快速开始

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash

# 启动 Gazebo 仿真
ros2 launch mybot_description gazebo_sim.launch.py
```

---

## 📝 学习记录

### 5月3日-5日：ROS2 基础节点、话题通信

### 5月13日：自定义消息接口

### 5月17日：URDF/Xacro 建模、FishBot 传感器模块化设计

### 5月18日：执行器建模、碰撞标签、Gazebo 仿真启动文件

### 5月19日：Gazebo 传感器插件配置

#### 核心概念

- **传感器类型（`<sensor type>`）**：Gazebo 通过不同的 type 区分物理传感器类型，如射线传感器（激光雷达）、IMU、深度相机等。type 决定了仿真引擎如何计算数据。
- **Gazebo 插件**：连接 Gazebo 仿真和 ROS2 话题的桥梁。不同传感器对应不同的插件库，插件负责将仿真数据转换为 ROS2 消息发布出去。
- **话题命名空间（`<namespace>`）**：为插件发布的所有话题统一添加前缀，避免多机器人场景下的命名冲突，也便于组织相关话题。
- **RViz 显示方式**：
  - **By Topic**：从话题出发，自动推荐合适的显示类型，适合快速查看仿真数据
  - **By Display Type**：从显示类型出发，手动指定话题，适合需要精细配置或话题列表未刷新时

#### 踩坑与解决思路

| 问题现象 | 排查思路 | 解决方法 |
|---------|---------|---------|
| 传感器话题完全不存在 | 先确认 URDF 中是否正确包含传感器配置，再检查插件是否被 Gazebo 正确加载 | 换用更稳定的插件实现；确保编译后重启 Gazebo |
| 修改配置后话题仍不更新 | Gazebo 运行时会缓存 URDF，launch 文件生成的临时文件也可能是旧的 | 彻底关闭所有相关进程后重新启动；清理临时文件 |
| RViz 中找不到话题 | 区分是话题不存在还是 RViz 未刷新 | 用命令行确认话题存在；RViz 中直接手动输入话题名 |
| 点云/图像显示异常 | 检查坐标系（Fixed Frame）是否正确，检查 TF 变换链是否完整 | 将 Fixed Frame 设为机器人本体坐标系；确认传感器 link 的 TF 已发布 |

#### 关键经验

1. **插件选择比配置更重要**：同一个传感器可能有多种插件实现，不同 ROS 版本的插件稳定性差异很大。遇到话题不发布的情况，优先考虑换插件。

2. **修改 URDF/Xacro 后必须重启 Gazebo**：Gazebo 在启动时加载 URDF，运行期间不会动态更新。任何模型修改都需要重新启动仿真才能生效。

3. **分层验证**：传感器不工作时，按层次排查——先确认话题是否存在（`ros2 topic list`），再确认是否有数据（`ros2 topic hz`），最后确认 RViz 是否能正确显示。

4. **命名空间 vs 重映射**：命名空间适合统一组织一个传感器的所有话题；重映射适合单独修改某个话题名。优先使用命名空间，代码更简洁。 

---

## 🔗 相关链接

- [ROS2 Humble 官方文档](https://docs.ros.org/en/humble/)
- [6-robot 官网](http://www.6-robot.com)
