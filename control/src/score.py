#!/usr/bin/env python


import rospy
import math
from geometry_msgs.msg import PoseStamped
from simple_pid import PID
from geometry_msgs.msg import Twist


class score_node:
    def __init__(self):
        rospy.init_node("score_node")
        rospy.loginfo("Calculating score")

        # ns = rospy.get_namespace()
        self.curr_pose = PoseStamped()
        self.target_pose = PoseStamped()
        self.curr_vel = Twist()
        
        #self.curr_pose.pose = rospy.wait_for_message(
        #       f'/{ns}/ground_truth/pose', Pose)

            #rospy.Subscriber('NAME OF TARGET X Y Z TOPIC', PoseStamped, self.target_callback)

        self.target_pose.pose.position.x=10
        self.target_pose.pose.position.y=0
        self.target_pose.pose.position.z=0

        rospy.Subscriber('/neo11/command/pose', PoseStamped, self.current_callback)
        self.pub = rospy.Publisher('/neo11/cmd_vel',Twist,queue_size=10)
        rospy.Timer(rospy.Duration(0.1),self.pub_callback)    
        self.print_score()
        self.calculate_vel()

    def target_callback(self, goal_pose):
        self.targetpose = goal_pose
    
    def current_callback(self, pose):
        self.curr_pose = pose
        self.print_score()

    def print_score(self):
        self.x_score= self.target_pose.pose.position.x - self.curr_pose.pose.position.x
        self.y_score= self.target_pose.pose.position.y - self.curr_pose.pose.position.y
        self.z_score= self.target_pose.pose.position.z - self.curr_pose.pose.position.z
        overall_score=math.sqrt(pow(self.x_score,2)+ pow(self.y_score,2) + pow(self.z_score,2))
        rospy.loginfo("Score x axis = %f Score y axis = %f Score z axis = %f Overall Score= %f \n",self.x_score,self.y_score,self.z_score,overall_score)

    def calculate_vel(self):
        pidx = PID(1, 0.1, 0.05, setpoint=self.x_score)
        pidy = PID(1, 0.1, 0.05, setpoint=self.y_score)
        pidz = PID(1, 0.1, 0.05, setpoint=self.z_score)

        self.curr_vel.linear.x=pidx
        self.curr_vel.linear.y=pidy
        self.curr_vel.linear.z=pidz
        self.curr_vel.angular=0

    def pub_callback(self, n):
        self.pub.publish(self.curr_vel)

if __name__ == "__main__":
    name_node = score_node()
    rospy.spin()
