# ROS2 学习工作空间

> 个人 ROS2 学习项目，基于 ROS2 Humble，涵盖 URDF 建模、节点编程、话题通信、仿真环境、ros2_control 控制等内容。

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
| `urdf/fishbot/fishbot.ros2_control.xacro` | ros2_control 硬件接口配置 |
| `config/ros2_control.yaml` | ros2_control 控制器参数配置 |
| `launch/dispaly_robot.launch.py` | RViz 显示启动文件 |
| `launch/gazebo_sim.launch.py` | Gazebo 仿真启动文件（自动加载控制器） |

### `wpr_simulation2` — 仿真综合包

来自 [6-robot](http://www.6-robot.com)，包含 SLAM、导航、机械臂控制等 demo。

---

## 🚀 快速开始

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash

# 启动 RViz 显示模型
ros2 launch mybot_description dispaly_robot.launch.py

# 启动 Gazebo 仿真（自动加载 ros2_control 控制器）
ros2 launch mybot_description gazebo_sim.launch.py
```

### 仿真中控制机器人运动

```bash
# 发布速度指令
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.5}, angular: {z: 0.0}}'

# 查看里程计
ros2 topic echo /odom

# 查看关节状态
ros2 topic echo /joint_states
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

### 5月20日：ros2_control 机器人控制框架

#### 核心概念

- **ros2_control**：ROS2 官方机器人控制框架，将硬件接口与控制器解耦，实现统一的机器人控制架构。
- **硬件接口（Hardware Interface）**：定义机器人关节的命令接口（Command Interface）和状态接口（State Interface）。FishBot 使用 `gazebo_ros2_control/GazeboSystem` 作为 Gazebo 仿真硬件接口。
- **命令接口（Command Interface）**：向硬件发送控制指令，如 `velocity`（速度控制）、`effort`（力矩控制）、`position`（位置控制）。
- **状态接口（State Interface）**：从硬件读取当前状态，如 `position`（位置）、`velocity`（速度）、`effort`（力矩）。
- **控制器（Controller）**：由 `controller_manager` 管理，负责具体的控制算法：
  - `diff_drive_controller/DiffDriveController`：差速驱动控制器，订阅 `/cmd_vel` 发布 `/odom`
  - `joint_state_broadcaster/JointStateBroadcaster`：关节状态广播器，发布 `/joint_states`
  - `effort_controllers/JointGroupEffortController`：力矩控制器，直接控制力矩输出
- **Controller Manager**：控制器管理器，负责控制器的加载、配置、启动和停止。

#### ros2_control 架构流程

```
用户指令 → /cmd_vel → diff_drive_controller → controller_manager
                                              ↓
                                    gazebo_ros2_control/GazeboSystem
                                              ↓
                                    Gazebo 物理引擎 → 关节运动
                                              ↓
                                    状态反馈 → /joint_states /odom
```

#### 关键文件说明

| 文件 | 作用 |
|------|------|
| `fishbot.ros2_control.xacro` | 定义 ros2_control 硬件接口，配置关节的命令/状态接口，加载 Gazebo 插件 |
| `ros2_control.yaml` | 配置 controller_manager 和具体控制器的参数 |
| `gazebo_sim.launch.py` | 启动 Gazebo 仿真，并通过事件处理器自动加载控制器 |

#### launch 文件中的事件处理机制

Gazebo 仿真启动后，需要等待机器人实体生成完成才能加载控制器。使用 `RegisterEventHandler` 实现链式加载：

1. `spawn_entity_node` 退出（机器人生成完成）→ 加载 `joint_state_broadcaster`
2. `joint_state_broadcaster` 加载完成 → 加载 `fishbot_diff_drive_controller`

```python
launch.actions.RegisterEventHandler(
    event_handler=launch.event_handlers.OnProcessExit(
        target_action=spawn_entity_node,
        on_exit=[action_load_joint_state_broadcaster],
    )
)
```

#### 踩坑与解决思路

| 问题现象 | 排查思路 | 解决方法 |
|---------|---------|---------|
| Gazebo 启动后立即崩溃（exit code -11） | 检查 ros2_control 配置是否正确，特别是插件参数路径 | 确保 `<parameters>` 指向具体的 YAML 文件，而非目录 |
| 控制器加载失败 | 检查 controller_manager 是否正常运行，确认 YAML 配置语法正确 | 使用 `ros2 control list_controllers` 查看状态；检查 YAML 缩进和参数名 |
| `/cmd_vel` 发布但机器人不动 | 确认 diff_drive_controller 是否已激活，检查关节名称是否匹配 | 用 `ros2 control list_controllers` 确认状态为 `active`；核对 URDF 中的关节名与 YAML 配置 |
| `/odom` 话题无数据 | 检查 diff_drive_controller 配置中的 `odom_frame_id` 和 `robot_base_frame` | 确保与 URDF 中的坐标系名称一致 |

#### 关键经验

1. **`<parameters>` 必须指向文件而非目录**：`gazebo_ros2_control` 插件的 `<parameters>` 标签需要指定具体的 YAML 文件路径。如果指向目录，Gazebo 会立即崩溃（段错误）。

2. **控制器加载时机很重要**：ros2_control 控制器必须在 Gazebo 完全启动且机器人实体生成后才能加载。使用 `OnProcessExit` 事件处理器确保正确的加载顺序。

3. **YAML 配置结构要正确**：`controller_manager` 下的控制器声明和独立的控制器参数块是分开的。前者声明类型，后者配置具体参数。

4. **关节名称必须全局一致**：URDF 中的关节名、`ros2_control.xacro` 中的关节名、`ros2_control.yaml` 中的关节名三者必须完全一致，否则控制器无法找到对应的关节。

5. **命令接口与控制器要匹配**：如果控制器期望 `velocity` 命令接口，但硬件接口只提供了 `effort`，控制器将无法正常工作。确保两者一致。

---

## 🔗 相关链接

- [ROS2 Humble 官方文档](https://docs.ros.org/en/humble/)
- [ros2_control 官方文档](https://control.ros.org/humble/doc/getting_started/getting_started.html)
- [6-robot 官网](http://www.6-robot.com)
