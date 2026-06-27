#pragma once

#include "clothes.h"
#include "outfit.grpc.pb.h"
#include <grpcpp/grpcpp.h>
#include <string>
#include <unordered_map>

class FitServ final : public outfit::FitAnalyzer::Service {
  private:
    std::unordered_map<int, RetailInfo> clothesData;

  public:
    FitServ();

    grpc::Status GetFitInfo(grpc::ServerContext *context, const outfit::ItemRequest *request,
                            outfit::RetailResponse *response) override;
};