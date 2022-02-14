#!/usr/bin/env python

import rospy
import numpy as np
import ros_numpy as rnp
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import CameraInfo
import sensor_msgs.point_cloud2 as pc2

class pcl_node:
    def __init__(self):
        self.search_p = [10,10]
        rospy.init_node("pcl_node")
        rospy.loginfo("Starting waypoint_node as name_node.")
        #ns = rospy.get_namespace()
        # self.lee_publisher = rospy.Publisher(
        #     f'/{ns}//', PointCloud2, queue_size=10)
        rospy.Subscriber('/neo11/vi_sensor/camera_depth/camera/camera_info', CameraInfo, self.cameraInfoCallback)
        rospy.Subscriber('/neo11/vi_sensor/camera_depth/depth/points', PointCloud2, self.pointsCallback)

    

    def rec_searchPoint(self, pc):
        middle = round(len(pc)/2)
        pc1 = np.transpose(pc[:middle])
        imagePoints = np.transpose(project_pc_to_image(pc1, self.P))
        if (len(pc) == 1): return pc
        elif self.search_p in imagePoints:
            return self.rec_searchPoint(pc[:middle])
        else: return self.rec_searchPoint(pc[middle :])

    def cameraInfoCallback(self, cameraInfo_data):
        print("got camera")
        P = cameraInfo_data.P
        self.P = [[P[0], P[1], P[2], P[3]], [P[4], P[5], P[6], P[7]], [P[8], P[9], P[10], P[11]]]
        # print(self.P)

    def pointsCallback(self, pcl_data):
        print("got pointcloud")
        self.pointCloud = rnp.point_cloud2.pointcloud2_to_xyz_array(pcl_data)
        self.goalPoint = self.rec_searchPoint(self.pointCloud)
        print(self.goalPoint)
        #self.lee_publisher.publish(goal_pose)


def project_pc_to_image(point_cloud, cam_p):
    pc_padded = np.append(point_cloud, np.ones((1, point_cloud.shape[1])), axis=0)
    pts_2d = np.dot(cam_p, pc_padded)
    pts_2d[0:2] = pts_2d[0:2] / pts_2d[2]
    return pts_2d[0:2]
      

if __name__ == "__main__":
    name_node = pcl_node()
    rospy.spin()
