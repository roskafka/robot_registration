import rclpy
import yaml
from rclpy.node import Node

from std_msgs.msg import String

from threading import Thread
from time import sleep

    
class RobotRegistration(Node):
    def __init__(self,robot_name,robot_type):
        self.robot_name=robot_name
        self.robot_type=robot_type

    def setup_callback(self):
        kafka_to_ros_yaml = self.setup_kafka_to_ros()
        ros_to_kafka_yaml = self.setup_ros_to_kafka()
        return(ros_to_kafka_yaml,kafka_to_ros_yaml)

    def get_generic_ros_to_kafka_mappings(self,yaml_path="exemplary_mappings.yaml"):
        with open(yaml_path,'r') as yamlfile:
          cur_yaml = yaml.safe_load(yamlfile) # Note the safe_load
        return cur_yaml["/ros_kafka_bridge"]["generic_mappings"][self.robot_type]

    def get_ros_to_kafka_values(self,yaml_path="exemplary_mappings.yaml"):
        generics= self.get_generic_ros_to_kafka_mappings()
        results={}
        for key, value in generics.items():
            newValue=value
            #alter from part
            to_kafka_replace_value="_"+self.robot_name+"_"
            to_ros_replace_value="/"+self.robot_name+"/"

            newValue['source']= newValue['source'].replace("/X/",to_ros_replace_value)
            newValue['destination']= newValue['destination'].replace("/X/",to_kafka_replace_value)
            results[self.robot_name+"/"+key]=newValue
        return results

    def setup_ros_to_kafka(self,generic_yaml_path="exemplary_mappings.yaml",active_yaml_path="example_ros_to_kafka.yaml"):
        with open(active_yaml_path,'r') as yamlfile:
            #get the current dictionary from the active vaml file and add the new data
            cur_yaml = yaml.safe_load(yamlfile) 
            new_dict=self.get_ros_to_kafka_values()
        #    cur_yaml["/ros_kafka_bridge"]["ros__parameters"]["mappings"].update(new_dict)
        #if cur_yaml:
        #    #save new data
        #    with open(active_yaml_path,'w') as yamlfile:
        #        yaml.safe_dump(cur_yaml, yamlfile) 
        return new_dict

    def get_generic_kafka_to_ros_mappings(self,yaml_path="exemplary_mappings.yaml"):
        with open(yaml_path,'r') as yamlfile:
          cur_yaml = yaml.safe_load(yamlfile) # Note the safe_load
        return cur_yaml["/kafka_ros_bridge"]["generic_mappings"][self.robot_type]


    def get_kafka_to_ros_values(self,yaml_path="exemplary_mappings.yaml"):
        generics= self.get_generic_kafka_to_ros_mappings()
        results={}
        for key, value in generics.items():
            
            newValue=value

            #alter from part
            to_kafka_replace_value="_"+self.robot_name+"_"
            to_ros_replace_value="/"+self.robot_name+"/"
            newValue['source']= newValue['source'].replace("/X/",to_kafka_replace_value)
            newValue['destination']= newValue['destination'].replace("/X/",to_ros_replace_value)
            results[self.robot_name+"/"+key]=newValue
        return results

    def setup_kafka_to_ros(self,generic_yaml_path="exemplary_mappings.yaml",active_yaml_path="example_kafka_to_ros.yaml"):
        with open(active_yaml_path,'r') as yamlfile:
            #get the current dictionary from the active vaml file and add the new data
            cur_yaml = yaml.safe_load(yamlfile) 
            new_dict=self.get_kafka_to_ros_values()
        #    cur_yaml["/kafka_ros_bridge"]["ros__parameters"]["mappings"].update(new_dict)
        #if cur_yaml:
        #    #save new data
        #    with open(active_yaml_path,'w') as yamlfile:
        #        yaml.safe_dump(cur_yaml, yamlfile)
        return new_dict 

        
        
def main(args=None):
    #registration=RobotRegistration("my_turtle","turtlesim")
    #print(registration.setup_callback())
    #print("here")
    pass


    

if __name__ == '__main__':
    main()
