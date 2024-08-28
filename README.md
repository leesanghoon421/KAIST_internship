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

