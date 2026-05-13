# Daily_ros2_study
Commit ros2 project in this repository
## 5月2日 新建年轻人的第一个Node节点
    采用面向对象的思想，新建一个node类
    我创建了一个发布者以及一个订阅者
## 5月3日 今天学习接口与服务
    新建接口需要的步骤
    1、创建接口包interface
        cd ~/ros2_ws/src
        ros2 pkg create --build-type ament_cmake interface
        mkdir interface/msg
    2、在interface/msg中编写消息定义文件
    3、配置 CMakeLists.txt
        find_package(rosidl_default_generators REQUIRED)

        rosidl_generate_interfaces(${PROJECT_NAME}
        "msg/Novel.msg"
        DEPENDENCIES sensor_msgs    # 如果 Novel.msg 用了 sensor_msgs 的类型
        )

        ament_package()
    4、配置 package.xml
        <build_depend>rosidl_default_generators</build_depend>
        <exec_depend>rosidl_default_runtime</exec_depend>
        <depend>sensor_msgs</depend>    <!-- 如果用了 sensor_msgs -->

        <member_of_group>rosidl_interface_packages</member_of_group>
    5、编译
        cd ~/ros2_ws
        colcon build --packages-select interface
        source install/setup.bash
## 5月4日 今天学习强化学习，明天继续ros
## 5月5日 学习服务
## 5月12日 今天主要学习使用numpy来表示位姿信息，并进行位姿变换
## 5月13日 仿真第一步，使用urdf新建一个模型用于后续仿真
