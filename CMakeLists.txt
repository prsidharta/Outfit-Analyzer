cmake_minimum_required(VERSION 3.15)
project(OutfitAnalyzerServer CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/server)

add_executable(server
    server/main.cpp
    server/FitServ.cpp
    server/outfit.pb.cc
    server/outfit.grpc.pb.cc
)

target_link_libraries(server PRIVATE
    gRPC::grpc++
    protobuf::libprotobuf
)