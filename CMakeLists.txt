cmake_minimum_required(VERSION 3.5.0)
project(RaytracerWeekend VERSION 0.1.0 LANGUAGES C CXX)

# Set the output directory
#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_executable(RaytracerWeekend src/main.cpp)

include(CTest)
enable_testing()

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
