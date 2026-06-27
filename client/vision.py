import grpc
import outfit_pb2
import outfit_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')

client = outfit_pb2_grpc.OutfitAnalyzerStub(channel)

test_id = 42
print(f"Sending Item ID {test_id} over the network...")

request = outfit_pb2.ItemRequest(item_id=test_id)

try:
    response = client.GetRetailInfo(request)
    
    print("\n C++ Data")
    print(f"Item:  {response.clothes_name}")
    print(f"Brand: {response.brand_name}")
    print(f"Price: ${response.price}")
    print(f"Link:  {response.purchase_link}")

except grpc.RpcError as e:
    print("\n[NETWORK ERROR]: C++ off. Python is working.")