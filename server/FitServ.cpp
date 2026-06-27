#include "FitServ.h"
#include <iostream>

FitServ::FitServ() {
    clothesData[0] = {"Red Shirt", "Nike", "nike.com/redshirt", 25.99};
}

grpc::Status FitServ::GetFitInfo(grpc::ServerContext *context, const outfit::ItemRequest *request,
                                 outfit::RetailResponse *response) {

    int itemId = request->item_id();

    if (auto it = clothesData.find(itemId); it != clothesData.end()) {

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