import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose, PoseStamped, Vector3, Quaternion, Point
from std_msgs.msg import ColorRGBA

class MarkerPublisher(Node):
    def __init__(self):
        super().__init__('marker_publisher')
        self.publisher_ = self.create_publisher(Marker, 'marker_topic', 10)
        self.subscription = self.create_subscription(
            Pose,
            'pose_communication',
            self.pose_callback,
            10)
        self.pose_msg = None  # Initialize pose message variable

        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.publish_marker)

    def pose_callback(self, msg):
        # Callback function to receive pose message from pose_communication topic
        self.get_logger().info('Received pose message')
        self.pose_msg = msg

    def publish_marker(self):
        self.get_logger().info('Publish marker called')
        if self.pose_msg is None:
            self.get_logger().warning('No pose message available')
            return

        # Extract position from Pose message
        position = self.pose_msg.position

        # Create PoseStamped message
        pose_stamped_msg = PoseStamped()
        pose_stamped_msg.header.stamp = self.get_clock().now().to_msg()
        pose_stamped_msg.header.frame_id = "map"  # Assuming frame_id is "map"
        pose_stamped_msg.pose.position = position
        pose_stamped_msg.pose.orientation = self.pose_msg.orientation

        # Create Marker message
        marker_msg = Marker()
        marker_msg.header.stamp = pose_stamped_msg.header.stamp
        marker_msg.header.frame_id = pose_stamped_msg.header.frame_id
        marker_msg.type = Marker.CUBE
        marker_msg.action = Marker.ADD
        marker_msg.pose = pose_stamped_msg.pose  # Use Pose from PoseStamped
        marker_msg.scale = Vector3(x=1.0, y=2.0, z=0.5)  # dimensions of the box (x, y, z)
        marker_msg.color = ColorRGBA(r=1.0, g=0.0, b=0.0, a=1.0)  # red color
        marker_msg.lifetime.sec = 1  # marker will only last 1 second

        self.publisher_.publish(marker_msg)
        self.get_logger().info('Published marker')

def main(args=None):
    rclpy.init(args=args)
    node = MarkerPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
