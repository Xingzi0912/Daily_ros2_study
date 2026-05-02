import rclpy
from rclpy.node import Node

# 编写ros2节点的一般步骤：
# 1. 导入rclpy库和Node类。
# 2. 创建一个继承自Node的类，定义节点的功能。
# 3. 在类的构造函数中初始化节点，并设置需要的参数、订阅者、发布者等。
# 4. 定义节点的回调函数，处理接收到的数据或执行定时任务。
# 5. 在main函数中初始化rclpy，创建节点实例，并调用rclpy.spin()来保持节点运行。 


class write_node(Node):
    def __init__(self,name):
        super().__init__('name')  # 调用父类构造函数，创建一个名为'write_node'的节点实例
        self.get_logger().info('大家好，我是%s' % name)  # 输出节点启动的日志信息
        # 在这里可以添加订阅者、发布者、定时器等功能

def main(args=None):
    # 入口函数，程序从这里开始执行 
    rclpy.init(args=args)  # 初始化rclpy库
    node = write_node('li4_node')  # 创建一个名为'li4_node'的节点实例
    rclpy.spin(node)  # 保持节点运行，等待回调函数被触发
    node.get_logger().info('li4_node has been shut down.')  # 输出节点关闭的日志信息
    node.destroy_node()  # 销毁节点实例
    rclpy.shutdown()  # 关闭rclpy库