from ultralytics import YOLOv10

model = YOLOv10('yolov10n.pt')

model.train(data='yolov10.yaml', epochs=500, batch=128, imgsz=640)