cmake_minimum_required(VERSION 3.5)
project(marrtinorobot2_navigation)

find_package(ament_cmake REQUIRED)
find_package(nav2_bringup REQUIRED)

install(
  DIRECTORY launch rviz config maps param
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
