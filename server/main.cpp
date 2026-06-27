
#include <unordered_map>
#include <string>
#include <iostream>
#include "clothes.h"

int main(){

    std::unordered_map<int, RetailInfo> clothesDatabase;
    std::vector<Clothes> seenClothes;

    clothesDatabase[0] = {"Red Shirt", "Nike", "nike.com/redshirt", 25.99};
    clothesDatabase[1] = {"Blue Jeans", "Levi's", "levi.com/bluejeans", 45.00};

    seenClothes.push_back({150, 200, 50, 100, 0, 0.95});
    seenClothes.push_back({300, 400, 60, 120, 99, 0.45});

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