cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_output_dirs_setup()

find_package(GumboParser REQUIRED)

include_directories(example ${GumboParser_INCLUDE_DIRS})
add_executable(example example.cpp)
target_link_libraries(example ${GumboParser_LIBRARIES})