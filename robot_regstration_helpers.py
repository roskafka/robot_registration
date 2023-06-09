import rclpy
import time
from roskafka_interfaces.srv import AddMapping
import mapping_aid
from collections import Counter

from std_msgs.msg import String

def fetch_mapping(robot_type="turtle_sim"):
    pass


def add_mappings_to_ros(robot_name,map_of_sensors,node):
    add_mappings(robot_name,map_of_sensors,node,mapping_type="kafka_ros")

def add_mappings_to_kafka(robot_name,map_of_sensors,node):
    print("k",map_of_sensors)

    add_mappings(robot_name,map_of_sensors,node,mapping_type="ros_kafka")
    
    
def add_mappings(robot_name,map_of_sensors,node,mapping_type):
    for sensor in map_of_sensors:
        print("registering with: ", map_of_sensors[sensor])
        # Create a client to the "add_mapping" service
        client = node.create_client(AddMapping, '/'+mapping_type+'/add_mapping')
        # Wait for the service to be available
        if not client.wait_for_service(timeout_sec=1.0):
            node.get_logger().info('Service not available')
            return
        # Create a request message
        print("s:",sensor,map_of_sensors[sensor])

        req = AddMapping.Request()
        req.name = robot_name
        req.source = map_of_sensors[sensor]["source"]
        req.destination = map_of_sensors[sensor]["destination"]
        req.type = map_of_sensors[sensor]["type"]

        # Call the service
        future = client.call_async(req)
        rclpy.spin_until_future_complete(node, future)

        # Process the response
        if future.result() is not None:
            node.get_logger().info(f'Result: {future.result().success}')
        else:
            node.get_logger().info('Service call failed')
            
def call_add_mapping_service(robot_name,robot_type,node):
    # Initialize the ROS node
    #rclpy.init()
    #node = rclpy.create_node('registration_node')

    #get correct mappings
    topic_mapper= mapping_aid.RobotRegistration(robot_name,robot_type)
    ros_to_kafka_mapings, kafka_to_ros_mappings=topic_mapper.setup_callback()

    print("to kafka")
    add_mappings_to_kafka(robot_name,ros_to_kafka_mapings,node)
    print("to ros")
    add_mappings_to_ros(robot_name,kafka_to_ros_mappings,node)


    # Shutdown the ROS node
    #node.destroy_node()
    #rclpy.shutdown()



def quick_test():
    #robot_name="my_new_robot"
    #topic_mapper= mapping_aid.RobotRegistration("my_turtle1","turtlesim")
    #ros_to_kafka_mapings, kafka_to_ros_mappings=mapping_aid.setup_callback(robot_name)
    #print(ros_to_kafka_mapings)
    #print(kafka_to_ros_mappings)

    call_add_mapping_service("dieter","turtlesim")
    call_add_mapping_service("klaus","turtlesim")

