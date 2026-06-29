cmake_minimum_required(VERSION 3.15)
project(OutfitAnalyzerServer CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/server)

add_custom_command(
    OUTPUT
        ${CMAKE_CURRENT_SOURCE_DIR}/server/outfit.pb.cc
        ${CMAKE_CURRENT_SOURCE_DIR}/server/outfit.pb.h
        ${CMAKE_CURRENT_SOURCE_DIR}/server/outfit.grpc.pb.cc
        ${CMAKE_CURRENT_SOURCE_DIR}/server/outfit.grpc.pb.h
    COMMAND protobuf::protoc
    ARGS --proto_path=${CMAKE_CURRENT_SOURCE_DIR}/proto
         --cpp_out=${CMAKE_CURRENT_SOURCE_DIR}/server
         --grpc_out=${CMAKE_CURRENT_SOURCE_DIR}/server
         --plugin=protoc-gen-grpc=$<TARGET_FILE:gRPC::grpc_cpp_plugin>
         ${CMAKE_CURRENT_SOURCE_DIR}/proto/outfit.proto
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/proto/outfit.proto
)

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