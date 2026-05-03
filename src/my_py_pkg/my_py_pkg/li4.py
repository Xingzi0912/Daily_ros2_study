import rclpy
from rclpy.node import Node
from std_msgs.msg import String, UInt32
from interface.msg import Novel


# 编写ros2节点的一般步骤：
# 1. 导入rclpy库和Node类。
# 2. 创建一个继承自Node的类，定义节点的功能。
# 3. 在类的构造函数中初始化节点，并设置需要的参数、订阅者、发布者等。
# 4. 定义节点的回调函数，处理接收到的数据或执行定时任务。
# 5. 在main函数中初始化rclpy，创建节点实例，并调用rclpy.spin()来保持节点运行。


class write_node(Node):
    def __init__(self, name):
        # 调用父类构造函数，创建一个名为'write_node'的节点实例
        super().__init__('name')
        self.get_logger().info('大家好，我是%s' % name)
        # 创建一个发布者，发布String类型的消息到'topic'主题，队列大小为10
        self.novel_publisher_ = self.create_publisher(String, 'man_what_can_i_say', 10)
        # 创建一个定时器，每隔4秒调用一次timer_callback函数
        self.timer = self.create_timer(4.0, self.timer_callback)
        # 创建一个订阅者，订阅UInt32类型的消息从'money'主题，队列大小为10
        self.sub_money_ = self.create_subscription(UInt32, 'kobe_money', self.money_callback, 10)
        self.account = 80


    def timer_callback(self):
        # 计数器，每次调用时增加1
        self.timer_count = getattr(self, 'timer_count', 0) + 1
        # 创建一个String类型的消息对象
        msg = String()
        # 设置消息内容
        msg.data = '这是第%d条李四发布的消息!' % self.timer_count
        # 发布消息到'topic'主题
        self.novel_publisher_.publish(msg)
        # 输出发布消息的日志信息
        self.get_logger().info('李四发布了一条消息：%s' % msg.data)

    def money_callback(self, money_msg):
        # 输出收到钱的日志信息
        self.get_logger().info('李四收到了一笔钱：%d' % money_msg.data)
        # 更新账户余额
        self.account += money_msg.data
        # 输出当前账户余额的日志信息
        self.get_logger().info('李四当前的账户余额是：%d' % self.account)


def main(args=None):
    # 入口函数，程序从这里开始执行
    # 初始化rclpy库
    rclpy.init(args=args)

    # 创建一个名为'li4_node'的节点实例
    node = write_node('li4_node')

    # 保持节点运行，等待回调函数被触发
    rclpy.spin(node)

    # 输出节点关闭的日志信息
    node.get_logger().info('li4_node has been shut down.')

    # 销毁节点实例
    node.destroy_node()

    # 关闭rclpy库
    rclpy.shutdown()
