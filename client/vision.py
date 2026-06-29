import grpc
import outfit_pb2
import outfit_pb2_grpc
import cv2

import numpy as np
from ultralytics import YOLO

import sys
import time

vid = cv2.VideoCapture(0)
channel = grpc.insecure_channel("localhost:50051")
client = outfit_pb2_grpc.FitAnalyzerStub(channel)

if not vid.isOpened():
    print("Could not open camera.")
    sys.exit()
print("Camera on. Press 'q' to quit.")

prev_time = 0
last_call = {"person": 0, "cell phone": 0}
cd_sec = 3.0
cache_data = None
model = YOLO("yolov8n.pt")

while True:
    ret, frame = vid.read()
    if not ret:
        print("Lost camera connection")
        break

    results = model(frame, verbose=False)
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        obj_name = model.names[cls_id]

        if obj_name in ["person", "cell phone"]:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            cur_time = time.time()
            if (cur_time - last_call[obj_name]) > cd_sec:
                try:
                    request = outfit_pb2.ItemRequest(det_obj=obj_name)
                    response = client.GetFitInfo(request)

                    cache_data = {
                        "name": response.clothes_name,
                        "brand": response.brand_name,
                        "price": f"${response.price:.2f}",
                    }
                    last_call[obj_name] = cur_time
                except grpc.RpcError:
                    print("C++ Server Offline.")
                    cache_data = None
            
            if cache_data:
                display_text = f"{cache_data['brand']} {cache_data['name']} - {cache_data['price']}"
                cv2.putText(
                    frame,
                    display_text,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

    new_time = time.time()
    fps = 1 / (new_time - prev_time)
    prev_time = new_time
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Outfit Analyzer", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        print("Exiting.")
        break

vid.release()
cv2.destroyAllWindows()