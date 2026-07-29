# TurtleBot3 Burger SLAM House Simulation

A ROS 2 package documenting the TurtleBot3 Burger SLAM simulation setup in a Gazebo house environment. This package features live online 2D mapping via `slam_toolbox`, pre-configured visualization in RViz2, and an intuitive custom Tkinter-based Teleop GUI controller.

<table>
  <tr>
    <td align="center"><b>Gazebo House Environment</b></td>
    <td align="center"><b>RViz2 2D Mapping (Complete)</b></td>
  </tr>
  <tr>
    <td><img src="docs/images/gazebo_house_world.png" alt="Gazebo House World" width="100%"></td>
    <td><img src="docs/images/rviz_map_complete.png" alt="RViz2 Complete Map" width="100%"></td>
  </tr>
</table>

---

## ROS 2 Distro Support

This repository follows standard ROS 2 conventions with separate branches for different ROS 2 distributions:

- **`main` branch**: ROS 2 Jazzy Jalisco (new Gazebo / `ros_gz`)
- **`humble` branch**: ROS 2 Humble Hawksbill (classic Gazebo / `gazebo_ros`)

To clone the **Humble** version:
```bash
git clone -b humble https://github.com/JosiahSK/turtlebot3_slam_house.git
```

---

## Features

- **Gazebo House World**: Loads the standard TurtleBot3 House simulation environment populated with walls, rooms, and obstacles.
- **2D Online SLAM**: Uses `slam_toolbox` (online async mode) with tuned mapping parameters.
- **RViz2 Visualization**: Automatically launches RViz2 pre-configured with Map, Robot Model, LaserScan, TF, and Footprint display plugins.
- **Custom GUI Teleop**: Includes a standalone Python Tkinter GUI featuring press-to-drive buttons, keyboard arrow key controls, spacebar emergency stop, and real-time speed sliders.

---

## Prerequisites

- **OS**: Ubuntu 24.04 LTS (or compatible Linux distribution)
- **ROS 2**: ROS 2 Jazzy Jalisco (or Humble / Iron)
- **Dependencies**:
  - `turtlebot3` packages (`turtlebot3`, `turtlebot3_simulations`, `turtlebot3_msgs`)
  - `slam_toolbox`
  - `rviz2`
  - Python 3 with `tkinter` (`sudo apt install python3-tk`)

---

## Installation & Setup

1. **Clone the repository** into your ROS 2 workspace `src` directory:
   ```bash
   cd ~/slam_ws/src
   git clone https://github.com/JosiahSK/turtlebot3_slam_house.git
   ```

2. **Build the workspace**:
   ```bash
   cd ~/slam_ws
   colcon build --symlink-install
   ```

---

## Quick Start / Launch Instructions

Source your ROS 2 environment, set the TurtleBot3 model, and execute the launch file:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
source install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_slam_house slam_house.launch.py
```

This single launch command brings up:
1. **Gazebo Simulator** with TurtleBot3 Burger spawned in the House world.
2. **`slam_toolbox`** node executing asynchronous 2D mapping.
3. **RViz2** displaying the live map generation.
4. **Teleop GUI Controller** for driving the robot.

---

## 2D SLAM Mapping in Progress

As the robot explores the environment, `slam_toolbox` processes laser scan data and wheel odometry to dynamically map out walls, doorways, and rooms:

![SLAM Mapping in Progress](docs/images/rviz_mapping_in_progress.png)

---

## Driving the Robot (Teleop Controller)

The custom Teleop GUI (`teleop_gui.py`) automatically opens upon launch.

<p align="center">
  <img src="docs/images/teleop_gui.png" alt="TurtleBot3 Teleop GUI Controller" width="380">
</p>

- **On-Screen Directional Buttons**: Click and hold **▲ UP**, **◄ LEFT**, **▼ DOWN**, or **► RIGHT** to steer.
- **Keyboard Arrow Keys**: Focus the GUI window and use the **Up**, **Down**, **Left**, and **Right** arrow keys.
- **Emergency Stop**: Click the red **STOP** button or press the **Spacebar** to immediately halt robot movement.
- **Speed Adjustment**: Adjust the **Linear Speed** (0.02 – 0.50 m/s) and **Angular Speed** (0.10 – 2.00 rad/s) sliders dynamically while driving.

---

## How to Save the Map

Once you have explored the environment and built a satisfactory map in RViz:

1. Open a new terminal and source the workspace:
   ```bash
   source /opt/ros/$ROS_DISTRO/setup.bash
   source ~/slam_ws/install/setup.bash
   ```

2. Save the map using `nav2_map_server`:
   ```bash
   mkdir -p maps
   ros2 run nav2_map_server map_saver_cli -f maps/my_house_map
   ```
   This will generate `my_house_map.yaml` and `my_house_map.pgm`.

> **Note**: The `maps/` directory and `.pgm` image files are intentionally listed in `.gitignore`. Maps are generated local artifacts and are kept out of version control so users can map and save their own custom sessions.

---

## How to Reset / Restart Mapping

If you want to start a fresh mapping session without restarting the entire simulation:

### Method 1: Quick Service / Node Reset
Clear the current map data in `slam_toolbox` via ROS 2 service:
```bash
ros2 service call /slam_toolbox/clear_changes slam_toolbox/srv/Clear
```
Alternatively, reset the `slam_toolbox` lifecycle node:
```bash
ros2 lifecycle set /slam_toolbox shutdown
ros2 lifecycle set /slam_toolbox configure
ros2 lifecycle set /slam_toolbox activate
```

### Method 2: Full Relaunch
Terminate the running launch command in your terminal (`Ctrl+C`) and re-run:
```bash
ros2 launch turtlebot3_slam_house slam_house.launch.py
```

---

## Project Structure

```text
turtlebot3_slam_house/
├── CMakeLists.txt                        # CMake build configuration
├── LICENSE                               # Apache License 2.0
├── package.xml                           # ROS 2 package metadata and dependencies
├── README.md                             # Project documentation
├── .gitignore                            # ROS 2 workspace git ignore definitions
├── config/
│   └── mapper_params_online_async.yaml   # SLAM Toolbox online async mapping parameters
├── docs/
│   └── images/                           # Screenshots and visuals
│       ├── gazebo_house_world.png
│       ├── rviz_mapping_in_progress.png
│       ├── rviz_map_complete.png
│       └── teleop_gui.png
├── launch/
│   └── slam_house.launch.py              # Main bringup launch file (Gazebo + SLAM + RViz2 + Teleop GUI)
├── rviz/
│   └── slam_house.rviz                   # Pre-configured RViz2 display layout
└── scripts/
    └── teleop_gui.py                     # Standalone Tkinter GUI teleop controller node
```

---

## Reference Package Versions & Branches

- **ROS 2 Distribution**: ROS 2 Jazzy Jalisco (Ubuntu 24.04 LTS)
- **`turtlebot3`**: `jazzy` branch
- **`turtlebot3_simulations`**: `jazzy` branch (`turtlebot3_gazebo` house world)
- **`turtlebot3_msgs`**: `jazzy` branch
- **`slam_toolbox`**: `jazzy` branch

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
