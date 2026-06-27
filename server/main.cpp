
#include "FitServ.h"
#include <grpcpp/grpcpp.h>
#include <iostream>
#include <memory>
#include <string>

void RunServ() {

    std::string servAddress("0.0.0.0:50051");
    FitServ service;
    grpc::ServerBuilder builder;

    builder.AddListeningPort(servAddress, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);

    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    std::cout << "[SERVER] Program listening on " << servAddress << std::endl;

    server->Wait();
}

int main(int argc, char **argv) {
    RunServ();
    return 0;
}