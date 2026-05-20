import os
import tempfile

import launch
import launch_ros
import xacro
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # 获取包路径
    pkg_share = get_package_share_directory('mybot_description')

    # xacro 文件路径
    xacro_file_path = os.path.join(pkg_share, 'urdf', 'fishbot', 'fishbot.urdf.xacro')
    gazebo_world_path = os.path.join(pkg_share, 'world', 'fish_world', 'fish_world_3.world')

    # 使用 xacro 生成 URDF
    doc = xacro.process_file(xacro_file_path)
    robot_description_xml = doc.toxml()
    temp_urdf_file = os.path.join(tempfile.gettempdir(), f'fishbot_{os.getpid()}.urdf')
    with open(temp_urdf_file, 'w', encoding='utf-8') as f:
        f.write(robot_description_xml)

    robot_description = {'robot_description': robot_description_xml}

    # 声明启动参数
    actions_declare_arg_model = launch.actions.DeclareLaunchArgument(
        name='model', default_value=str(xacro_file_path), description='加载的 xacro 模型路径'
    )

    # robot_state_publisher：发布机器人 TF
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description],
    )

    # 启动 Gazebo
    gazebo_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]
        ),
        launch_arguments={'world': gazebo_world_path}.items(),
    )

    # 在 Gazebo 中生成机器人实体
    spawn_entity_node = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=['-file', temp_urdf_file, '-entity', 'fishbot', '-x', '0.0', '-y', '0.0', '-z', '0.1', '-package_to_model'],
    )

    # 加载并激活 joint_state_broadcaster 控制器
    # ros2 control load_controller joint_state_broadcaster --set-state active
    action_load_joint_state_broadcaster = launch.actions.ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', 'joint_state_broadcaster', '--set-state', 'active'],
        output='screen',
    )

    # #激活fishbot_ros2_control系统控制器
    # action_load_fishbot_effort_controller = launch.actions.ExecuteProcess(
    #     cmd=['ros2', 'control', 'load_controller', 'fishbot_effort_controller', '--set-state', 'active'],
    #     output='screen',
    # )

    #激活diff_drive_controller系统控制器
    action_load_diff_drive_controller = launch.actions.ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', 'fishbot_diff_drive_controller', '--set-state', 'active'],
        output='screen',
    )   



    return launch.LaunchDescription(
        [
            actions_declare_arg_model,
            robot_state_publisher_node,
            gazebo_launch,
            spawn_entity_node,
            launch.actions.RegisterEventHandler(
                event_handler=launch.event_handlers.OnProcessExit(
                    target_action=spawn_entity_node,
                    on_exit=[action_load_joint_state_broadcaster],
                )
            ),
            launch.actions.RegisterEventHandler(
                event_handler=launch.event_handlers.OnProcessExit(
                    target_action=action_load_joint_state_broadcaster,
                    on_exit=[action_load_diff_drive_controller],
                )
            ),
        ]
    )
