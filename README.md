This is a proof of consept for "2022 IEEE Autonomous Unmanned Aerial Vehicles (UAV) Competition"

We got short on time and our work is not complete. We managed to test each part seperately and it worked pretty well, but when we tried to combine each part, we couldn't make it work.


# UAVChase Initialize project

1)install dependencies
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-latest.list'
wget http://packages.ros.org/ros.key -O - | sudo apt-key add -
sudo apt-get update
sudo apt-get install ros-noetic-desktop-full ros-noetic-joy ros-noetic-octomap-ros ros-noetic-mavlink python-wstool python-catkin-tools protobuf-compiler libgoogle-glog-dev ros-noetic-control-toolbox ros-noetic-mavros

sudo rosdep init
rosdep update
source /opt/ros/noetic/setup.bash
```


2)Create workspace
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
git clone https://github.com/ethz-asl/rotors_simulator
catkin_init_workspace  # initialize your catkin workspace
wstool init
wget https://raw.githubusercontent.com/ethz-asl/rotors_simulator/master/rotors_hil.rosinstall
wstool merge rotors_hil.rosinstall
wstool update
```

3)build 
```
cd ~/catkin_ws/
catkin build
```
4)add sources to bashrc
```
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
5)τεστ

if everything works fine then it should open gazebo and the drone should hover.
``` 
roslaunch rotors_gazebo mav_hovering_example.launch mav_name:=firefly world_name:=basic
```

6)trial worlds

Follow the steps of the repository https://github.com/Hunter314/uavcc-simulator:

Step 1: Open terminal in the trial_1_setup folder and run the following commands
```
mkdir build
cd build
cmake ../
make
```
Step 2: Copy and Paste this on the terminal inside trial_1_setup/build/ and press enter:
```
echo "export GAZEBO_PLUGIN_PATH=`pwd`:$GAZEBO_PLUGIN_PATH" >> ~/.bashrc
```
Step 3: Run the environment/world in gazebo
```
cd ~/trial_1_setup
gazebo trial_1.world
```
The world of the simulator should open with a moving rover.

8)gazebo models

copy and paste all mmodels from the trial_1_setup to the dir ~/.gazebo/models

7)UAVChase
```
cd ~/catkin_ws/src
git clone https://github.com/markostamos/UAVChase
cd ~/catkin_Ws
catkin build
```

8)Test

```
roslaunch uav_sim trial1.launch

```
It should open rviz and gazebo.


# Control


# Vision
The part of the computer vision of the drone was conducted using the camera image. For the trial 1 and 2 we used an ord detection algorithm that takes advantage of the color of the orb. We used the HSV parameters of the image in order to transform the image and extract only the x,y orb_center. First, we took sample images from the camera looking the rover and manualy find the prefered HSV (min,max) parameters. Then, we took in real time the image_raw from our drone and calculate the orb in the x,y camera frame.
In order to calculate the 3D x,y,z point of the orbit we constructed a recuring function that transforms the 3D point cloud into a 2D frame in the exact point of the camera. The function tries to match each 3D point from the point Cloud of the drone to the 2D point of the camera frame. Then we pass the target point into a topic in order for the control team to use it to direct the drone.
We managed to write each code individualy but ended up not be able to connect them before the deadline.
