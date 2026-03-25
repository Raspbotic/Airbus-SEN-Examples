cmake_minimum_required(VERSION 3.20 FATAL_ERROR)

project(simulation_adapter_project VERSION 0.1.0 LANGUAGES CXX C)

# 1. Locate SEN (Assumes SEN_PATH is set in your environment)
if(DEFINED ENV{SEN_PATH})
   list(APPEND CMAKE_PREFIX_PATH "$ENV{SEN_PATH}/cmake")
endif()

find_package(sen REQUIRED)

# 2. Define the Consolidated Adapter Package
# This creates 'simulation_interface_package.dll'
add_sen_package(
  TARGET simulation_interface_package
  MAINTAINER "KapBotics"
  VERSION "0.1.0"
  SOURCES 
    src/simulation_interface.h 
    src/simulation_interface.cpp
  STL_FILES 
    stl/sim_interface/simulation_interface.stl
)

# 3. Export settings for Windows compatibility
set_target_properties(simulation_interface_package PROPERTIES 
    LINK_FLAGS "/OPT:NOREF" 
    WINDOWS_EXPORT_ALL_SYMBOLS ON
)