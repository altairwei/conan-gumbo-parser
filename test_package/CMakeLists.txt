cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_output_dirs_setup()

find_package(Gumbo REQUIRED)

include_directories(example ${Gumbo_INCLUDE_DIRS})
add_executable(example example.cpp)
target_link_libraries(example ${Gumbo_LIBRARIES})