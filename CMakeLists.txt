cmake_minimum_required(VERSION 3.8)
project(turtlebot3_slam_house)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  scripts/teleop_gui.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME teleop_gui
)

install(DIRECTORY launch rviz config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
