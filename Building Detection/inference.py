import cv2
from ultralytics import YOLOv10

# 학습된 모델 로드
model = YOLOv10("runs/detect/train/weights/best.pt")

def draw_bounding_boxes(image_path, results, output_image_path, output_coords_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    
    bounding_boxes = results[0].boxes.xyxy.cpu().numpy()  # 바운딩 박스 좌표
    confidences = results[0].boxes.conf.cpu().numpy()     # 신뢰도
    class_ids = results[0].boxes.cls.cpu().numpy()        # 클래스 ID
    
    with open(output_coords_path, 'w') as f:
        for bbox, conf, cls_id in zip(bounding_boxes, confidences, class_ids):
            x_min, y_min, x_max, y_max = bbox
            cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (255, 0, 0), 2)
            
            # 바운딩 박스 좌표 저장
            f.write(f"{cls_id} {conf} {x_min/width} {y_min/height} {x_max/width} {y_max/height}\n")
    
    cv2.imwrite(output_image_path, image)

# 추론할 이미지 경로
source_image_path = 'images/roadview4.png'
output_image_path = 'upgrade_output/roadview4.png'
output_coords_path = 'upgradebb_output/roadview4.txt'

# 추론 수행
results = model(source_image_path)

# 바운딩 박스를 그려서 이미지와 좌표를 저장
draw_bounding_boxes(source_image_path, results, output_image_path, output_coords_path)