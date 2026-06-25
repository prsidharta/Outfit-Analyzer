
#pragma once

#include <string>
#include <vector>

struct Clothes {

    int c_x;
    int c_y;
    int c_width;
    int c_height;
    int c_type;
    double c_accuracy;

};

struct RetailInfo{

    std::string r_clothesName;
    std::string r_brandName;
    std::string r_purchaseLink;
    double r_price;

};