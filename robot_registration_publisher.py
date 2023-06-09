import rclpy
import time
from roskafka_interfaces.srv import AddMapping
import mapping_aid
from collections import Counter
from rclpy.node import Node
from std_msgs.msg import String
import robot_regstration_helpers as registration



class RobotRegistrationNode(Node):

    def __init__(self):
        super().__init__('robot_registration_node')
        self.publisher_ = self.create_publisher(String, '/robotRegistration', 10)
        
        self.registration_callback("turtlesim","dieter")
        #self.registration_callback("turtlesim","klaus")
        
        input_value=""
        while(input_value != "stop" ):
            
            input_value=input("enter a new robot_type/robot_name pair")
            if input_value=="stop" :
                break
            name=input_value.split("/")[1]
            type=input_value.split("/")[0]
            self.registration_callback(type,name)
       

    def registration_callback(self,robot_type,robot_name):
        msg = String()
        msg.data = robot_type+"/"+robot_name
        self.publisher_.publish(msg)
        time.sleep(1)
        registration.call_add_mapping_service(robot_name=robot_name,robot_type=robot_type,node=self)



def main(args=None):
    rclpy.init(args=args)
    node = RobotRegistrationNode()
    rclpy.spin(node)
    print("pess enter to close Node")
    input()
    rclpy.shutdown()

if __name__ == '__main__':
    main()