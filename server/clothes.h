
#pragma once

#include <vector>

struct Clothes {

    int c_x;
    int c_y;
    int c_width;
    int c_height;
    int c_type;
    double c_accuracy;
};

// Size 368 bytes for this struct
struct RetailInfo {

    char r_clothesName[50];
    char r_brandName[50];
    char r_purchaseLink[256];
    double r_price;
};