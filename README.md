# KAIST_internship
Retrieving Info of Building by Building detection, Long distance estimation, GS1 GEO dataset

This project is part of AILEE 2025 - City Sensing AI projects v2

This project is divided into four main stages:

## 1. Building Detection
![화면 캡처 2024-08-06 143038](https://github.com/user-attachments/assets/1a64bdeb-996a-4b28-a091-2dae6ff42c32)

inference.py code in Building Detection folder can detect building and make bounding box. 

## 2. Distance Prediction to Buildings
![화면 캡처 2024-08-06 143631](https://github.com/user-attachments/assets/d55c6042-27ee-4349-9f28-7f670fc149b0)

DPT github: [https://github.com/isl-org/DPT](https://github.com/isl-org/DPT)
download pretrained weight(dpt_hybrid-midas-501f0c75.pt)

## 3. Calculation of Building GPS Coordinates Using Vehicle GPS Information and Distance Data

![distance_test](https://github.com/user-attachments/assets/2aae5f23-622a-49fb-99cc-2c7be4d896b6)

reference point: 5m point

## 4. Providing Detailed Information on Buildings by Connecting with GS1 GEO Data


