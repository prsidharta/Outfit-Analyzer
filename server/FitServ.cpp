#include "FitServ.h"
#include <iostream>

FitServ::FitServ() {
    clothesData["person"] = {"Red Shirt", "Nike", "nike.com/redshirt", 25.99};
    clothesData["cell phone"] = {"Black Beanie", "Carhartt", "carhartt.com/beanie", 19.99};
}

grpc::Status FitServ::GetFitInfo(grpc::ServerContext *context, const outfit::ItemRequest *request,
                                 outfit::RetailResponse *response) {

    std::string detObj = request->det_obj();
    std::cout << "Detected: " << detObj << std::endl;

    if (auto it = clothesData.find(detObj); it != clothesData.end()) {

        auto item = it->second;
        response->set_clothes_name(item.r_clothesName);
        response->set_brand_name(item.r_brandName);
        response->set_purchase_link(item.r_purchaseLink);
        response->set_price(item.r_price);

        return grpc::Status::OK;
    } else {
        return grpc::Status(grpc::StatusCode::NOT_FOUND, "Item not found");
    }
}