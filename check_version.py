import torch
import pickle

checkpoint = torch.load('best.pt', map_location='cpu', pickle_module=pickle)

print(checkpoint.keys())  # 모델 체크포인트의 키들을 출력
