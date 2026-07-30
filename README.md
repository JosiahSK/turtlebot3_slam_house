# TurtleBot3 Burger SLAM House Simulation (ROS 2 Humble Branch)

A ROS 2 package documenting the TurtleBot3 Burger SLAM simulation setup in a Gazebo house environment. This package features live online 2D mapping via `slam_toolbox`, pre-configured visualization in RViz2, and an intuitive custom Tkinter-based Teleop GUI controller.

> [!NOTE]
> **ROS 2 Distro Support**: This is the **`humble`** branch configured for **ROS 2 Humble** and **Classic Gazebo** (`gazebo_ros` / `gazebo_plugins`).
> For ROS 2 Jazzy (Gazebo Sim / `ros_gz`), please switch to the [`main`](https://github.com/JosiahSK/turtlebot3_slam_house/tree/main) branch.

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

## Features

- **Gazebo House World**: Loads the standard TurtleBot3 House simulation environment in Classic Gazebo populated with walls, rooms, and obstacles.
- **2D Online SLAM**: Uses `slam_toolbox` (online async mode) with tuned mapping parameters.
- **RViz2 Visualization**: Automatically launches RViz2 pre-configured with Map, Robot Model, LaserScan, TF, and Footprint display plugins.
- **Custom GUI Teleop**: Includes a standalone Python Tkinter GUI featuring press-to-drive buttons, keyboard arrow key controls, spacebar emergency stop, and real-time speed sliders.

---

## Prerequisites

- **OS**: Ubuntu 22.04 LTS (Jammy Jellyfish)
- **ROS 2**: ROS 2 Humble Hawksbill
- **Simulator**: Classic Gazebo (Gazebo 11 / `gazebo_ros_pkgs`, `gazebo_plugins`)
- **Dependencies**:
  - `gazebo_ros_pkgs` (`sudo apt install ros-humble-gazebo-ros-pkgs`)
  - `turtlebot3` packages (`turtlebot3`, `turtlebot3_simulations`, `turtlebot3_msgs`) — `humble` branch
  - `slam_toolbox` (`sudo apt install ros-humble-slam-toolbox`)
  - `rviz2`
  - Python 3 with `tkinter` (`sudo apt install python3-tk`)

---

## Installation & Setup

1. **Clone the repository** into your ROS 2 workspace `src` directory on the `humble` branch:
   ```bash
   cd ~/slam_ws/src
   git clone -b humble https://github.com/JosiahSK/turtlebot3_slam_house.git
   ```

2. **Install TurtleBot3 Humble dependencies**:
   ```bash
   cd ~/slam_ws/src
   git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3.git
   git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
   git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
   ```

3. **Install system dependencies via rosdep**:
   ```bash
   cd ~/slam_ws
   rosdep update
   rosdep install --from-paths src --ignore-src -r -y
   ```

4. **Build the workspace**:
   ```bash
   cd ~/slam_ws
   colcon build --symlink-install
   ```

---

## Full Build & Launch Steps (Humble)

1. Note that the package must sit inside a `src/` folder of a workspace, e.g.:
   ```text
   ~/slam_ws/src/turtlebot3_slam_house/
   ```

2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-tk
   cd ~/slam_ws
   rosdep install --from-paths src --ignore-src -r -y
   ```

3. Build the workspace:
   ```bash
   cd ~/slam_ws
   colcon build --symlink-install
   ```

4. Source the environment:
   ```bash
   source /opt/ros/humble/setup.bash
   source ~/slam_ws/install/setup.bash
   ```

5. Set the TurtleBot3 model:
   ```bash
   export TURTLEBOT3_MODEL=burger
   ```

6. Launch everything:
   ```bash
   ros2 launch turtlebot3_slam_house slam_house.launch.py
   ```

7. If the launch fails, verify the package is visible:
   ```bash
   ros2 pkg list | grep turtlebot3_slam_house
   ```

---

## Quick Start / Launch Instructions

Source your ROS 2 Humble environment, set the TurtleBot3 model, and execute the launch file:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_slam_house slam_house.launch.py
```

This single launch command brings up:
1. **Classic Gazebo Simulator** (`gazebo_ros`) with TurtleBot3 Burger spawned in the House world (`spawn_entity.py`).
2. **`slam_toolbox`** node executing asynchronous 2D mapping.
3. **RViz2** displaying the live map generation.
4. **Teleop GUI Controller** for driving the robot.

---

## Known Limitations & Verification Note

> [!IMPORTANT]
> **Untested on Live ROS 2 Humble Machine**:
> This branch was updated to target ROS 2 Humble and Classic Gazebo (`gazebo_ros` / `gazebo_plugins`) based on official Humble package specifications and APIs. However, because the development host machine only has ROS 2 Jazzy installed, end-to-end launch and build execution on this branch could not be verified on a live ROS 2 Humble environment.
> If running on ROS 2 Humble, please verify that topic names (e.g. `/cmd_vel`, `/scan`, `/odom`, `/tf`) and spawning behavior function as expected.

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
   source /opt/ros/humble/setup.bash
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

- **ROS 2 Distribution**: ROS 2 Humble Hawksbill (Ubuntu 22.04 LTS)
- **`turtlebot3`**: `humble` branch
- **`turtlebot3_simulations`**: `humble` branch (`turtlebot3_gazebo` house world)
- **`turtlebot3_msgs`**: `humble` branch
- **`slam_toolbox`**: `humble` branch

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).

---

## 📘 ROS 2 Humble Study Guide (For Students)

Welcome to the beginner study guide! If you are a student brand new to robotics, Linux terminals, or ROS 2, this guide is written specifically for you. Think of this section as your friendly Teaching Assistant (TA) holding office hours—we will break down complex concepts into simple ideas, use real-world analogies, and connect everything directly to the code in this `turtlebot3_slam_house` repository.

---

### 1. What is ROS 2?

Imagine building a modern autonomous robot, like a self-driving vacuum cleaner or a Mars rover. A robot is not just one single software program running on a computer; it is a team of specialized software components working together. You have sensors (like laser scanners and camera sensors), motors driving the wheels, navigation algorithms planning paths, and user interfaces displaying live maps. ROS 2, which stands for **Robot Operating System 2**, is the software framework that connects all of these separate pieces together seamlessly.

Despite its name, ROS 2 is not a traditional operating system like Windows, macOS, or Linux. You cannot install ROS 2 on a bare computer without an OS already present. Instead, ROS 2 runs on top of your existing operating system (specifically Linux Ubuntu 22.04 LTS for ROS 2 Humble) as **middleware**—plumbing software that sits between your operating system and your robot application code. Think of middleware as a universal translation layer: it allows a Python script controlling a graphical user interface to speak effortlessly to a C++ program controlling motor drivers or processing high-speed lidar sensor data, even if those programs run on completely different chips or physical computers.

Why do robots need ROS 2? Without middleware like ROS 2, every robotics engineer would have to write custom network socket protocols, sensor data serializers, and thread scheduling logic from scratch every time they wanted to build a robot. ROS 2 provides standardized messaging tools, sensor data formats, coordinate transformation libraries, and simulation interfaces so you can focus on building intelligent robot behavior instead of reinventing basic computer communication.

> **✅ Checkpoint**
> 
> **Question**: Is ROS 2 an operating system like Linux or Windows that boots up your computer hardware?
> 
> **Answer**: No! ROS 2 is **middleware** (a set of software libraries and communication tools) that runs on top of an existing operating system like Ubuntu Linux to help different robot software components communicate with each other.

> **🛠️ Try It Yourself**
> 
> Verify that ROS 2 Humble is properly installed and active on your system by checking the `$ROS_DISTRO` environment variable in your terminal:
> ```bash
> source /opt/ros/humble/setup.bash
> echo $ROS_DISTRO
> ```
> *Expected output*: `humble`

---

### 2. Core Building Blocks

To understand how ROS 2 operates, let us explore its five core building blocks using real-world analogies and concrete examples from this repository.

#### Node (A Single Running Program)
- **Definition**: A **Node** is a single running process (a standalone computer program) that performs one specific job in a robotics system. For instance, one node might read data from a laser scanner, while another node controls wheel speeds.
- **Analogy**: Think of nodes as individual chefs in a restaurant kitchen: one chef chops vegetables, one chef grills meat, and a dishwasher washes plates. Each worker focuses on one specific job, but together they produce full meals.
- **Concrete Example**: In `turtlebot3_slam_house`, `scripts/teleop_gui.py` runs as a dedicated node named `teleop_gui`. Its sole job is to display a graphical window, capture your button clicks or arrow key presses, and translate them into movement commands.

> **✅ Checkpoint**
> 
> **Question**: Why does ROS 2 break a robot system into many small nodes instead of writing one giant program?
> 
> **Answer**: Modular design makes system components isolated and reusable! If one node crashes (for instance, if your graphical user interface closes), other critical nodes (like emergency safety braking or sensor processing) continue running safely, and you can swap out components without rewriting your entire codebase.

#### Topic (A Communication Channel)
- **Definition**: A **Topic** is a named data channel used for asynchronous communication between nodes. A node that produces data sends messages to a topic as a **Publisher**, while a node that wants to read that data listens to the topic as a **Subscriber**.
- **Analogy**: Imagine a radio station broadcasting on a specific frequency (channel). The radio station DJ is the *publisher*, broadcasting music without needing to know who is listening. Anyone who tunes their radio to that frequency is a *subscriber*, receiving the music in real-time.
- **Concrete Example**: The `teleop_gui` node acts as a **Publisher** that publishes speed velocity commands onto the topic `/cmd_vel` (using the message type `geometry_msgs/msg/Twist`). The Gazebo simulator (or physical robot motor controller) acts as a **Subscriber** to `/cmd_vel`, listening for those velocity commands to turn the robot's physical wheels.

> **✅ Checkpoint**
> 
> **Question**: If a publisher node publishes data onto a topic, does it need to know which specific subscriber nodes are listening?
> 
> **Answer**: No! Communication over topics is completely decoupled. Publishers simply broadcast data to the topic name, and subscribers listen to the topic name, allowing nodes to operate independently without knowing about each other's existence.

#### Package (An Organized App Folder)
- **Definition**: A **Package** is an organized directory containing ROS 2 code, configuration files, launch scripts, custom message definitions, and build manifests (`package.xml` and `CMakeLists.txt`). It is the fundamental unit of code distribution in ROS 2.
- **Analogy**: Think of a package like a specific software app downloaded from an app store (like Spotify or VS Code). It contains all the code, assets, and settings needed for that specific application to work.
- **Concrete Example**: `turtlebot3_slam_house` is a ROS 2 package! It bundles together the launch script (`launch/slam_house.launch.py`), mapping configuration (`config/mapper_params_online_async.yaml`), RViz display layout (`rviz/slam_house.rviz`), and teleoperation GUI (`scripts/teleop_gui.py`).

> **✅ Checkpoint**
> 
> **Question**: What two essential files must be present at the root of a folder to make ROS 2 recognize it as a valid package?
> 
> **Answer**: `package.xml` (which defines package metadata and dependencies) and a build file like `CMakeLists.txt` (for CMake packages) or `setup.py` (for pure Python packages).

#### Workspace (Your Project Binder)
- **Definition**: A **Workspace** is a dedicated directory on your computer where you clone, edit, compile, and manage one or more ROS 2 packages together.
- **Analogy**: A workspace is like a student's project binder for a class. Inside your binder (`slam_ws`), you keep multiple subject folders (`turtlebot3_slam_house`, `slam_toolbox`, `turtlebot3`). When you build your workspace, you build all the packages inside your binder at once.
- **Concrete Example**: `~/slam_ws` is our ROS 2 workspace. Inside `~/slam_ws/src/`, we store our package `turtlebot3_slam_house` alongside related dependencies.

> **✅ Checkpoint**
> 
> **Question**: Can a single ROS 2 workspace contain more than one package inside its `src/` folder?
> 
> **Answer**: Yes! A workspace `src/` folder can hold as many packages as you need for your project, and the build tool (`colcon build`) will automatically compile all of them in dependency order.

#### Launch File (The Conductor)
- **Definition**: A **Launch file** is a Python, XML, or YAML script that automates starting multiple ROS 2 nodes, setting environment variables, and loading parameter files with a single command.
- **Analogy**: Think of a launch file as an orchestra conductor who raises their baton and signals all instruments (nodes) to start playing together at the exact right moment.
- **Concrete Example**: `launch/slam_house.launch.py` is our master bringup launch file. Instead of opening 5 separate terminals to manually launch Gazebo, `robot_state_publisher`, `slam_toolbox`, `rviz2`, and `teleop_gui.py`, one launch command starts all of them together.

> **✅ Checkpoint**
> 
> **Question**: What happens if you attempt to execute a launch file without sourcing `install/setup.bash` first?
> 
> **Answer**: ROS 2 will not be able to locate the package or its launch file, resulting in a `PackageNotFoundError`.

> **🛠️ Try It Yourself**
> 
> List all packages currently recognized in your ROS 2 environment:
> ```bash
> source /opt/ros/humble/setup.bash
> source ~/slam_ws/install/setup.bash
> ros2 pkg list | grep turtlebot3
> ```
> *Expected output*: You will see `turtlebot3_slam_house` and other installed TurtleBot3 packages listed in your terminal.

---

### 3. Anatomy of This Workspace

Now let us step inside the folder structure of `~/slam_ws` to understand how files are compiled, organized, and launched.

```text
slam_ws/                        # Workspace root directory
├── src/                        # SOURCE SPACE: Human-written code lives here
│   └── turtlebot3_slam_house/  # Our ROS 2 package
├── build/                      # BUILD SPACE: Temporary compilation files
├── install/                    # INSTALL SPACE: Compiled binaries and runnable scripts
└── log/                        # LOG SPACE: Build log files for debugging
```

#### Why `src/`, `build/`, `install/`, and `log/` Exist
- **`src/` (Source space)**: This is the **only** directory where you write and edit code! You clone Git repositories or place custom package folders inside `src/`.
- **`build/` (Build space)**: Created automatically when you run `colcon build`. It stores intermediate build files (like object code `.o` files and CMake build caches). You never need to edit files in `build/`.
- **`install/` (Install space)**: Created automatically by `colcon build`. Contains finished executable binaries, Python scripts, launch files, and setup scripts (`install/setup.bash`). Sourcing `install/setup.bash` updates your environment variables (`PATH`, `PYTHONPATH`, `AMENT_PREFIX_PATH`) so ROS 2 can find your compiled packages.
- **`log/` (Log space)**: Contains text logs produced by `colcon` during compilation, which are helpful when diagnosing build errors.
- **What `colcon build` does**: `colcon` reads each package's manifest files in `src/`, computes the build dependency order, compiles C++ binaries, copies or symlinks Python scripts into `install/`, and generates environment setup scripts.

#### Manifest Files: `package.xml` vs `CMakeLists.txt`
Every ROS 2 package has two fundamental files that tell the system how to treat its contents:

- **`package.xml` (The Package Passport)**: Declares package metadata (name, version, author, license) and lists all software dependencies. For example, `package.xml` in `turtlebot3_slam_house` lists `<exec_depend>slam_toolbox</exec_depend>` and `<exec_depend>rviz2</exec_depend>`. When you run `rosdep install`, ROS 2 reads `package.xml` to automatically download missing packages via `apt`.
- **`CMakeLists.txt` (The Build Blueprint)**: Contains step-by-step compilation and installation instructions for the CMake build engine. In `turtlebot3_slam_house`, `CMakeLists.txt` tells `colcon` to copy `scripts/teleop_gui.py` into `lib/turtlebot3_slam_house/` and copy the `launch/`, `rviz/`, and `config/` folders into `share/turtlebot3_slam_house/`.

#### Node-by-Node Walkthrough of `launch/slam_house.launch.py`
When you execute `ros2 launch turtlebot3_slam_house slam_house.launch.py`, ROS 2 executes a Python script that orchestrates 6 key processes:

```text
                                [ teleop_gui node ]
                                         │
                                         ▼ (publishes velocity commands)
                                    /cmd_vel
                                         │
                                         ▼
[ Gazebo Simulator ] ───► /scan ───► [ slam_toolbox ] ───► /map ───► [ RViz2 Visualization ]
  (Physics & Robot)       (Lidar)      (2D Mapping)         (Grid)     (3D Dashboard)
         │                                   ▲
         └──────────────► /tf ───────────────┘
                     (Odometry)
```

1. **`set_tb3_model`**: Exports the environment variable `TURTLEBOT3_MODEL=burger` so all downstream launch files know which robot model to load.
2. **`turtlebot3_house_cmd` (Gazebo & Robot State)**:
   - **Gazebo Simulator**: Starts the 3D physics simulator, loading the standard Gazebo House world populated with walls, doors, and furniture.
   - **`spawn_entity`**: Reads the TurtleBot3 Burger URDF (Unified Robot Description Format) XML file and spawns the 3D robot model into Gazebo at coordinates `(0, 0, 0)`.
   - **`robot_state_publisher`**: Publishes the robot's 3D kinematic structure and transformation frame tree (`/tf`), linking wheel movements (`odom`) to the robot's base chassis (`base_footprint`) and lidar sensor (`base_scan`).
3. **`slam_toolbox_cmd` (`slam_toolbox` node)**:
   - Starts the asynchronous 2D mapping node using settings from `config/mapper_params_online_async.yaml`. It subscribes to `/scan` (lidar data from Gazebo) and `/tf` (robot movement), running graph-based SLAM algorithms to output the live occupancy grid map on topic `/map`.
4. **`rviz2_cmd` (`rviz2` node)**:
   - Launches RViz2 pre-loaded with `rviz/slam_house.rviz`. It subscribes to `/map`, `/scan`, and `/tf` to display a live 3D visual dashboard of the robot and generated map on your screen.
5. **`teleop_gui_cmd` (`scripts/teleop_gui.py` node)**:
   - Launches our custom Python Tkinter interface. When you press key arrows or click buttons, it publishes `Twist` velocity messages to `/cmd_vel`, which Gazebo receives to drive the virtual robot wheels.

> **✅ Checkpoint**
> 
> **Question**: Which folder in your ROS 2 workspace should you directly edit code in?
> 
> **Answer**: `src/`! The `build/` and `install/` directories are automatically generated by `colcon build` and will be overwritten whenever you rebuild your workspace.

> **🛠️ Try It Yourself**
> 
> Rebuild your workspace using `colcon build` to observe how `colcon` processes packages in `src/`:
> ```bash
> cd ~/slam_ws
> colcon build --symlink-install
> ```
> *Expected output*: `colcon` will compile your packages and report `Summary: X packages finished`.

---

### 4. Essential CLI Commands

Here is a breakdown of the seven essential command-line tools you will use every day in ROS 2.

#### 1. Sourcing the ROS 2 Environment
```bash
source /opt/ros/humble/setup.bash
```
- **Syntax Breakdown**:
  - `source`: Bash command that executes script commands in your current terminal session without opening a subshell.
  - `/opt/ros/humble/setup.bash`: Absolute file path to the system-installed ROS 2 Humble setup file.
- **Under the Hood**: Populates essential system environment variables (`PATH`, `LD_LIBRARY_PATH`, `PYTHONPATH`, `AMENT_PREFIX_PATH`, `ROS_DISTRO=humble`) so your terminal can recognize commands like `ros2`, `colcon`, and system ROS libraries.

#### 2. Building the Workspace
```bash
colcon build --symlink-install
```
- **Syntax Breakdown**:
  - `colcon`: The standard ROS 2 command-line build tool manager.
  - `build`: Subcommand instructing colcon to compile packages inside `src/`.
  - `--symlink-install`: Optional flag creating symbolic links (shortcuts) to non-compiled files (like Python scripts, launch files, and YAML configs) in `install/`.
- **Under the Hood**: Reads manifest files in `src/`, compiles C++ code, and links Python/launch files into `install/`. The `--symlink-install` flag is a huge time-saver: edits made to Python scripts or launch files take effect immediately without needing to rerun `colcon build`!

#### 3. Executing a Launch File
```bash
ros2 launch turtlebot3_slam_house slam_house.launch.py
```
- **Syntax Breakdown**:
  - `ros2`: Main CLI entrypoint for ROS 2 tools.
  - `launch`: Subcommand used to run launch files.
  - `turtlebot3_slam_house`: Name of the target package.
  - `slam_house.launch.py`: Name of the launch file inside the package `share/` directory.
- **Under the Hood**: Locates the installed launch script in `install/turtlebot3_slam_house/share/turtlebot3_slam_house/launch/`, evaluates its node launch definitions, sets environment variables, and launches all specified nodes concurrently.

#### 4. Running a Single Node
```bash
ros2 run turtlebot3_slam_house teleop_gui
```
- **Syntax Breakdown**:
  - `ros2`: Main ROS 2 CLI tool.
  - `run`: Subcommand used to start a single node executable.
  - `turtlebot3_slam_house`: Package name.
  - `teleop_gui`: Name of the installed executable binary or script.
- **Under the Hood**: Looks up the package binary directory in `install/turtlebot3_slam_house/lib/turtlebot3_slam_house/` and executes `teleop_gui` as a single standalone process.

#### 5. Inspecting Topics and Live Messages
```bash
ros2 topic list
ros2 topic echo /cmd_vel
```
- **Syntax Breakdown**:
  - `ros2 topic list`: Lists all active topic channels currently registered across all running nodes.
  - `ros2 topic echo`: Creates a temporary command-line subscriber node listening to a specific topic.
  - `/cmd_vel`: Target topic name to intercept.
- **Under the Hood**: Queries the ROS 2 graph discovery network. `ros2 topic echo` initializes a hidden node, subscribes to `/cmd_vel`, deserializes binary network packets into human-readable text, and prints published velocity data live to your terminal.

#### 6. Listing Available Packages
```bash
ros2 pkg list
```
- **Syntax Breakdown**:
  - `ros2`: Main ROS 2 CLI tool.
  - `pkg`: Subcommand for querying package information.
  - `list`: Command argument to print all discovered packages.
- **Under the Hood**: Scans all directories registered in `$AMENT_PREFIX_PATH` (including `/opt/ros/humble/` and `~/slam_ws/install/`) and prints an alphabetical list of all valid ROS 2 packages found.

#### 7. Automatically Installing System Dependencies
```bash
rosdep install --from-paths src --ignore-src -r -y
```
- **Syntax Breakdown**:
  - `rosdep`: ROS dependency manager tool.
  - `install`: Command argument instructing rosdep to install missing packages.
  - `--from-paths src`: Instructs rosdep to scan `package.xml` files inside `src/`.
  - `--ignore-src`: Skips installing dependencies if the package itself is present inside `src/`.
  - `-r`: Recursive flag; continues installing even if a specific package encounters an error.
  - `-y`: Automatically answers "yes" to all Linux `apt` confirmation prompts.
- **Under the Hood**: Parses `<depend>`, `<exec_depend>`, and `<build_depend>` tags across all `package.xml` files in `src/`, maps ROS dependency keys to Linux Ubuntu `apt` package names (e.g. `ros-humble-slam-toolbox`), and invokes `sudo apt-get install` to install missing packages automatically.

> **✅ Checkpoint**
> 
> **Question**: Why is the `--symlink-install` flag so useful when running `colcon build` during Python development?
> 
> **Answer**: It creates symbolic links to Python scripts and launch files in the `install/` directory instead of copying them. This means edits made to Python files in `src/` take effect immediately without requiring a rebuild!

> **🛠️ Try It Yourself**
> 
> Practice inspecting active ROS 2 topics in your workspace (make sure you source your workspace setup file first!):
> ```bash
> source /opt/ros/humble/setup.bash
> source ~/slam_ws/install/setup.bash
> ros2 topic list
> ```
> *Expected output*: A list of active system topics in your ROS 2 environment.

---

### 5. Troubleshooting Lab

Below are six common "mysteries" students encounter when building and launching ROS 2 projects. Test your debugging skills by trying to guess the cause before reading the fix!

#### Mystery 1: `PackageNotFoundError: turtlebot3_gazebo`
```text
[ERROR] [launch]: Package ["turtlebot3_gazebo"] not found
```
- **Guess the Cause**: 
  *(Pause and think: Why would ROS 2 fail to find a package?)*

- **Explanation & Fix**:
  - **Cause**: The ROS 2 launch system cannot find `turtlebot3_gazebo` because either: (1) the TurtleBot3 simulation packages were not cloned into `src/`, or (2) you forgot to source your workspace setup script (`source ~/slam_ws/install/setup.bash`).
  - **Fix**: Clone the missing TurtleBot3 simulation repositories into `src/`, build, and source your workspace:
    ```bash
    cd ~/slam_ws/src
    git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
    cd ~/slam_ws
    colcon build --symlink-install
    source ~/slam_ws/install/setup.bash
    ```

#### Mystery 2: `install/setup.bash: No such file or directory`
```text
bash: ~/slam_ws/install/setup.bash: No such file or directory
```
- **Guess the Cause**: 
  *(Pause and think: Why would the install directory be missing?)*

- **Explanation & Fix**:
  - **Cause**: The `install/` folder does not exist yet because you have not compiled your workspace with `colcon build`.
  - **Fix**: Navigate to your workspace root directory and run `colcon build`:
    ```bash
    cd ~/slam_ws
    colcon build --symlink-install
    source ~/slam_ws/install/setup.bash
    ```

#### Mystery 3: `InvalidFrontendLaunchFileError`
```text
launch.invalid_launch_file_error.InvalidFrontendLaunchFileError: The launch file was not found or is invalid
```
- **Guess the Cause**: 
  *(Pause and think: Why would colcon fail to install a launch file?)*

- **Explanation & Fix**:
  - **Cause**: You either misspelled the launch file name in your command, or `CMakeLists.txt` is missing the instruction to install the `launch/` directory into `share/`.
  - **Fix**: Check `CMakeLists.txt` to ensure `install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})` is present, rebuild, and re-source:
    ```bash
    cd ~/slam_ws
    colcon build --symlink-install
    source ~/slam_ws/install/setup.bash
    ros2 launch turtlebot3_slam_house slam_house.launch.py
    ```

#### Mystery 4: `E: Unable to locate package` (apt / universe repository issue)
```text
E: Unable to locate package ros-humble-gazebo-ros-pkgs
```
- **Guess the Cause**: 
  *(Pause and think: Why would Linux apt fail to find a valid ROS package?)*

- **Explanation & Fix**:
  - **Cause**: Ubuntu's `universe` software repository is disabled on your Linux installation, or your `apt` package index is out of date.
  - **Fix**: Enable the `universe` repository, update `apt`, and install the package:
    ```bash
    sudo apt-get install software-properties-common
    sudo add-apt-repository universe
    sudo apt update
    sudo apt install ros-humble-gazebo-ros-pkgs
    ```

#### Mystery 5: Gazebo Stuck on `"Preparing your world..."`
```text
[gazebo-1] [INFO] [1700000000.000000000] [gazebo]: Preparing your world...
(Gazebo window stays black or unresponsive for several minutes)
```
- **Guess the Cause**: 
  *(Pause and think: What is Gazebo downloading in the background on first launch?)*

- **Explanation & Fix**:
  - **Cause**: On its very first run, Classic Gazebo attempts to download 3D model meshes (sun, ground, furniture) from an online server. If your internet connection is slow or firewalled, Gazebo hangs while waiting for downloads.
  - **Fix**: Pre-clone the Gazebo model database into your local `~/.gazebo/models` folder:
    ```bash
    mkdir -p ~/.gazebo/models
    git clone https://github.com/osrf/gazebo_models.git ~/.gazebo/models
    ```

#### Mystery 6: `TURTLEBOT3_MODEL is not set`
```text
[ERROR] [launch]: TURTLEBOT3_MODEL is not set. Please export TURTLEBOT3_MODEL=burger (or waffle/waffle_pi)
```
- **Guess the Cause**: 
  *(Pause and think: How does TurtleBot3 know which robot model to load?)*

- **Explanation & Fix**:
  - **Cause**: TurtleBot3 packages require the `TURTLEBOT3_MODEL` environment variable to determine which robot URDF model dimensions and sensor offsets to load into simulation.
  - **Fix**: Export the model variable in your terminal session before launching:
    ```bash
    export TURTLEBOT3_MODEL=burger
    ros2 launch turtlebot3_slam_house slam_house.launch.py
    ```

> **✅ Checkpoint**
> 
> **Question**: What should be your very first troubleshooting step if a `ros2 launch` command claims a ROS 2 package cannot be found?
> 
> **Answer**: Check if you sourced the workspace setup script (`source ~/slam_ws/install/setup.bash`) in your active terminal session!

> **🛠️ Try It Yourself**
> 
> Practice setting your `TURTLEBOT3_MODEL` environment variable and printing its value:
> ```bash
> export TURTLEBOT3_MODEL=burger
> echo $TURTLEBOT3_MODEL
> ```
> *Expected output*: `burger`

---

### 6. End-of-Guide Quiz

Test your understanding of ROS 2 Humble fundamentals with these five questions!

1. **Question 1 (Nodes)**: What is a ROS 2 node, and why is it beneficial to build a robot using multiple small nodes instead of one large monolithic script?
2. **Question 2 (Topics & Communication)**: In the `turtlebot3_slam_house` package, which node acts as the *publisher* on the `/cmd_vel` topic, and which node acts as the *subscriber*?
3. **Question 3 (Workspace Structure)**: Why should you only write and edit source code inside the `src/` folder of your workspace, rather than inside `build/` or `install/`?
4. **Question 4 (CLI & Sourcing)**: What is the exact purpose of running `source ~/slam_ws/install/setup.bash` after running `colcon build`?
5. **Question 5 (Launch Files)**: What is a ROS 2 launch file, and how does `launch/slam_house.launch.py` help launch a full simulation?

---

#### Quiz Answer Key

1. **Answer 1**: A ROS 2 node is a single running process that handles one specific task (e.g., teleoperation, SLAM, visualization). Breaking a robot into small nodes promotes modularity, code reuse, and system fault tolerance—if one node crashes, the rest of the robot can keep running.
2. **Answer 2**: The `teleop_gui` node (`scripts/teleop_gui.py`) acts as the **publisher** on `/cmd_vel`, broadcasting speed velocity commands. The **Gazebo simulator** (specifically the differential drive motor plugin) acts as the **subscriber** listening to `/cmd_vel` to move the virtual robot wheels.
3. **Answer 3**: `src/` is the only folder meant for human-written source code. The `build/` and `install/` folders are generated automatically by `colcon build` during compilation and will be overwritten or erased whenever the workspace is rebuilt or cleaned.
4. **Answer 4**: Sourcing `install/setup.bash` updates your terminal environment variables (`PATH`, `PYTHONPATH`, `AMENT_PREFIX_PATH`) so your system and ROS 2 command-line utilities can find the packages, binaries, executables, and launch files compiled inside your workspace.
5. **Answer 5**: A ROS 2 launch file is a script (usually in Python) that automates starting multiple nodes, setting parameters, and configuring environment variables simultaneously. `slam_house.launch.py` brings up Gazebo, `robot_state_publisher`, `slam_toolbox`, `rviz2`, and `teleop_gui` with a single command.
