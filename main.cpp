
#include <unordered_map>
#include <iostream>
#include "clothes.h"

int main(){

    std::unordered_map<int, RetailInfo> clothesDatabase;
    std::vector<Clothes> seenClothes;

    for (const auto &item : seenClothes){
        auto it = clothesDatabase.find(item.c_type);
        if (it == clothesDatabase.end()){
            std::cout << "Item Unavailable" << "\n";
            continue;
        }

        std::cout << "Found " << it->second.r_clothesName << 
        ". It costs $" << it->second.r_price << 
        " and can be found at " << it->second.r_purchaseLink << "\n";
    }

    return 0;
}