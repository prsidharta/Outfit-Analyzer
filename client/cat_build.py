import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import json
import os

print("Initial CLIP download")

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

print("Successful CLIP initialization")


def get_image(image_path):
    if not os.path.exists(image_path):
        print(f"ERROR: {image_path} does not exist.")
        return []

    image = Image.open(image_path).convert("RGB")
    input = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        features = model.get_image_features(**input)

        if not isinstance(features, torch.Tensor):
            features = features.pooler_output

    features = features / features.norm(p=2, dim=-1, keepdim=True)
    return features[0].tolist()


if __name__ == "__main__":
    print("Processing images.")

    catalog = {
        "item_1": {
            "name": "Mets Jersey",
            "brand": "Nike",
            "price": 149.99,
            "link": "https://www.mlbshop.com/new-york-mets/mens-new-york-mets-juan-soto-nike-white-home-replica-jersey/t-36778775+p-462269452194771+z-9-3360347106?_ref=p-DLP:m-GRID:i-r2c0:po-6",
            "vector": get_image("mets_jersey.jpg"),
        },
        "item_2": {
            "name": "'47 Mets Hat",
            "brand": "47",
            "price": 35.00,
            "link": "https://www.47brand.com/products/new-york-mets-47-clean-up-2",
            "vector": get_image("mets_hat.jpg"),
        },
        "item_3": {
            "name": "Brown Nike Vomero 5s",
            "brand": "Nike",
            "price": 170.00,
            "link": "https://www.nike.com/t/zoom-vomero-5-mens-shoes-MgsTqZ/FB9149-006",
            "vector": get_image("nike_shoes.jpg"),
        },
    }

    with open("catalog.json", "w") as f:
        json.dump(catalog, f, indent=4)
        print("Successful catalog dump.")
