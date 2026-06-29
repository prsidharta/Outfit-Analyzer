import grpc
import outfit_pb2
import outfit_pb2_grpc
import cv2

import sys
import numpy as np
import time


vid = cv2.VideoCapture(0)
channel = grpc.insecure_channel('localhost:50051')
client = outfit_pb2_grpc.FitAnalyzerStub(channel)

if not vid.isOpened():
    print("Could not open camera.")
    sys.exit()
print("Camera on. Press 'q' to quit.")

last_call = 0
cd_sec = 3.0
cache_data = None

while True:
    ret, frame = vid.read()
    if not ret:
            print ("Lost camera connection")
            break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([136, 87, 111])
    upper_red = np.array([180, 255, 255])
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
         area = cv2.contourArea(contour)

         if area > 8000:
              x, y, w, h = cv2.boundingRect(contour)
              cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 3)

              cur_time = time.time()
              if (cur_time - last_call) > cd_sec:
                   try:
                        request = outfit_pb2.ItemRequest(item_id = 0)
                        response = client.GetFitInfo(request)

                        cache_data = {
                             "name": response.clothes_name,
                             "brand": response.brand_name,
                             "price": f"${response.price:.2f}"
                        }
                        last_call = cur_time
                   except grpc.RpcError:
                        print("C++ Server Offline.")
                        cache_data = None
              if cache_data:
                display_text = f"{cache_data['brand']} {cache_data['name']} - {cache_data['price']}"
                cv2.putText(frame, display_text, (x, y - 10),
                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
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
