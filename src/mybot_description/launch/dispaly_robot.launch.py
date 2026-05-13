import os

import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Get the path to the URDF file
    urdf_file_path = os.path.join(get_package_share_directory('mybot_description'), 'urdf', 'mybot.urdf')

    # 声明启动参数，指定URDF模型路径
    actions_declare_arg_model = launch.actions.DeclareLaunchArgument(
        name='model', 
        default_value=str(urdf_file_path), 
        description='加载的URDF模型路径'
    )

    # Create a node to publish the robot description
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': open(urdf_file_path).read()}],
    )

    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher', 
        executable='joint_state_publisher', 
        name='joint_state_publisher', 
        output='screen'
    )

    # Create a node to launch RViz
    rviz_node = launch_ros.actions.Node(
        package='rviz2', 
        executable='rviz2', 
        name='rviz2', 
        output='screen'
    )

    return launch.LaunchDescription([
        actions_declare_arg_model, 
        robot_state_publisher_node, 
        joint_state_publisher_node, 
        rviz_node
    ])
