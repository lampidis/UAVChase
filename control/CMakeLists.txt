cmake_minimum_required(VERSION 3.0.2)
project(control)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  tf
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES control
#  CATKIN_DEPENDS rospy
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)


catkin_install_python(PROGRAMS
   src/vel_controller_node.py
   src/rviz_goal_publisher_node.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
 )



install(DIRECTORY src DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

