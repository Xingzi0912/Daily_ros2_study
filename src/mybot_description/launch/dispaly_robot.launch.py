import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command  # 新增导入

def generate_launch_description():
    xacro_file_path = os.path.join(
        get_package_share_directory('mybot_description'), 
        'urdf', 
        'fishbot',
        'fishbot.urdf.xacro'
    )
    
    default_rviz_config_path = os.path.join(
        get_package_share_directory('mybot_description'), 
        'config', 
        'my_display_config.rviz'
    )
    
    # 声明启动参数
    actions_declare_arg_model = launch.actions.DeclareLaunchArgument(
        name='model',
        default_value=str(xacro_file_path),
        description='加载的URDF模型路径'
    )
    
    # 使用 Command 在运行时解析 xacro
    robot_description = Command(['xacro ', xacro_file_path])
    
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}],
    )
    
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen'
    )
    
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', default_rviz_config_path]
    )
    
    return launch.LaunchDescription([
        actions_declare_arg_model,
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node
    ])