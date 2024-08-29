# KAIST_internship
Retrieving Info of Building by Building detection, Long distance estimation, GS1 GEO dataset

This project is part of AILEE 2025 - City Sensing AI projects v2

### Simple program running
run zed_record.py -> zed x mini gets image and reference point

run data_connect.py -> can get result

# Project Flow

![그림1](https://github.com/user-attachments/assets/e88dbe8b-729d-4813-aadc-83634a538970)


## 1. Building Detection
![화면 캡처 2024-08-06 143038](https://github.com/user-attachments/assets/1a64bdeb-996a-4b28-a091-2dae6ff42c32)

inference.py code in Building Detection folder can detect building and make bounding box. 

## 2. Distance Prediction to Buildings
![화면 캡처 2024-08-06 143631](https://github.com/user-attachments/assets/d55c6042-27ee-4349-9f28-7f670fc149b0)

DPT github: [https://github.com/isl-org/DPT](https://github.com/isl-org/DPT)
download pretrained weight(dpt_hybrid-midas-501f0c75.pt)

## 3. Calculation of Building GPS Coordinates Using Vehicle GPS Information and Distance Data

![화면 캡처 2024-08-28 163025](https://github.com/user-attachments/assets/bea89d76-5c94-4e38-8550-bdd6a318d599)


![화면 캡처 2024-08-28 162839](https://github.com/user-attachments/assets/d7c1f760-76f4-4d1c-a4a5-e1e01f926b9e)



## 4. Providing Detailed Information on Buildings by Connecting with GS1 GEO Data

![화면 캡처 2024-08-28 163118](https://github.com/user-attachments/assets/87d6b704-676a-4389-be01-3ea302553df5)





## AILEE 차량 테스트를 위한 정보

기본적으로는 simple program running에 따라 zed_record를 실행하면 이미지와 reference point를 저장합니다.
이때 현재 reference point는 5m지점으로 되어있지만 차량에서 테스트를 진행해보며 너무 가깝게 예측하는 경우 reference point를 줄이고 너무 멀게 예측하는경우 reference point를 늘려야합니다.

reference point를 조절하는 방법은 zed_record.py 코드에서 reference_point 변수를 바꾸고 (mm단위) distance_specify.py 코드에서 reference_distance를 수정해야합니다. 이때 (reference_distance)^3 = reference_point 조건을 만족시키도록 수정해야합니다.

예를들어 reference_point를 5미터로 한다면 1.7의 세제곱이 약 5이므로 referece_distance를 1.7로 바꿔주어야 합니다.


다음으로 data_connect.py 코드를 실행시켜 결과를 보기 전에 모든 이미지와 중간 저장 데이터들이 담기는 폴더들을 비우고 진행하시는 것을 추천드립니다.

+) 필요한 개선사항

1. 데이터를 연속적으로 입력받고 결과를 출력할 수 있도록 개선해야 더욱 유용한 시스템이 될 것 같습니다.

2. heading, car GPS를 실시간으로 입력받을 수 있도록 해야합니다.

3. 카메라 설치 위치를 개선하여 차량 전면부(hood)가 카메라에 담기지 않아야 distance estimation에 악영향이 없을 것으로 보입니다.

