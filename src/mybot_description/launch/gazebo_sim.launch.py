import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command

def generate_launch_description():
    # 获取包路径
    pkg_share = get_package_share_directory('mybot_description')
    
    # xacro 文件路径
    xacro_file_path = os.path.join(pkg_share, 'urdf', 'fishbot', 'fishbot.urdf.xacro')
    gazebo_world_path = os.path.join(pkg_share, 'world', 'fish_world', 'fish_world_1.world')

    # 使用 xacro 生成 URDF
    robot_description = Command(['xacro ', xacro_file_path])
    
    # 声明启动参数
    actions_declare_arg_model = launch.actions.DeclareLaunchArgument(
        name='model',
        default_value=str(xacro_file_path),
        description='加载的 xacro 模型路径'
    )
    
    # robot_state_publisher：发布机器人 TF
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}],
    )
    
    # 启动 Gazebo
    gazebo_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ]),
        launch_arguments={'world': gazebo_world_path}.items()
    )
    
    # 在 Gazebo 中生成机器人实体
    spawn_entity_node = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'fishbot',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1'
        ],
    )
    
    return launch.LaunchDescription([
        actions_declare_arg_model,
        robot_state_publisher_node,
        gazebo_launch,
        spawn_entity_node,
    ])
