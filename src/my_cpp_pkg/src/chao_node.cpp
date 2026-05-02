#include "rclcpp/rclcpp.hpp"

class SingleDogNode : public rclcpp::Node
{
private:
    // 这里可以添加成员变量和函数

public:
    SingleDogNode(std::string name) : Node(name)
    {
        RCLCPP_INFO(this->get_logger(), "大家好！我是%s，我正在学习ROS2。", name.c_str());
    }
};  





int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SingleDogNode>("wang2_node");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
   
