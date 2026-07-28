import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_turtlebot3_gazebo = get_package_share_directory('turtlebot3_gazebo')
    pkg_slam_toolbox = get_package_share_directory('slam_toolbox')
    pkg_turtlebot3_slam_house = get_package_share_directory('turtlebot3_slam_house')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Ensure TURTLEBOT3_MODEL environment variable is exported as burger
    set_tb3_model = SetEnvironmentVariable('TURTLEBOT3_MODEL', 'burger')

    # 1. Gazebo House World + Spawner + Robot State Publisher + GZ ROS Parameter Bridge
    turtlebot3_house_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_turtlebot3_gazebo, 'launch', 'turtlebot3_house.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # 2. SLAM Toolbox Online Async Mode
    slam_params_file = os.path.join(pkg_turtlebot3_slam_house, 'config', 'mapper_params_online_async.yaml')
    slam_toolbox_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_slam_toolbox, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'slam_params_file': slam_params_file
        }.items()
    )

    # 3. RViz2 pre-configured with SLAM display configuration
    rviz_config_dir = os.path.join(pkg_turtlebot3_slam_house, 'rviz', 'slam_house.rviz')
    rviz2_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_dir],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # 4. Standalone Teleop GUI Controller Node
    teleop_gui_cmd = Node(
        package='turtlebot3_slam_house',
        executable='teleop_gui',
        name='teleop_gui',
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(set_tb3_model)
    ld.add_action(turtlebot3_house_cmd)
    ld.add_action(slam_toolbox_cmd)
    ld.add_action(rviz2_cmd)
    ld.add_action(teleop_gui_cmd)

    return ld
