import grpc
import outfit_pb2
import outfit_pb2_grpc
import cv2
import sys

vid = cv2.VideoCapture(0)
channel = grpc.insecure_channel('localhost:50051')
client = outfit_pb2_grpc.FitAnalyzerStub(channel)

if not vid.isOpened():
    print("Could not open camera.")
    sys.exit()
print("Camera on. Press 'q' to quit.")

while True:
    ret, frame = vid.read()

    if not ret:
            print ("Lost camera connection")
            break
    cv2.imshow("Outfit Analyzer", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
         print("Exiting.")
         break

    elif key == ord('s'):
        test_id = 0
        print(f"Sending Item ID {test_id} over the network...")
        request = outfit_pb2.ItemRequest(item_id=test_id)
        try:
            response = client.GetFitInfo(request)
            print("\n C++ Data")
            print(f"Item:  {response.clothes_name}")
            print(f"Brand: {response.brand_name}")
            print(f"Price: ${response.price}")
            print(f"Link:  {response.purchase_link}")
        except grpc.RpcError as e:
            print("\n[NETWORK ERROR]: C++ off. Python is working.")


vid.release()
cv2.destroyAllWindows()
