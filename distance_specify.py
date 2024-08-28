import numpy as np
import matplotlib.pyplot as plt
import os
import glob

def load_pfm(file_path):
    with open(file_path, "rb") as f:
        header = f.readline().decode('latin-1').rstrip()
        color = header == 'PF'
        
        dims = f.readline().decode('latin-1')
        width, height = map(int, dims.split())
        
        scale = float(f.readline().decode('latin-1').rstrip())
        if scale < 0:
            endian = '<'
            scale = -scale
        else:
            endian = '>'
        
        data = np.fromfile(f, endian + 'f')
        shape = (height, width, 3) if color else (height, width)
        
        return np.reshape(data, shape), scale

def calculate_absolute_distance(pfm_path, ref_point, ref_distance):
    depth_map, scale = load_pfm(pfm_path)
    height, width = depth_map.shape[:2]

    # 참조 지점의 깊이 값 및 최대 깊이 값 계산
    ref_depth_value = depth_map[ref_point[1], ref_point[0]]
    max_depth_value = np.max(depth_map)

    # 디버깅용 출력
    print(f"Depth map max: {max_depth_value}")
    print(f"Reference point: {ref_point}")
    print(f"Reference depth value: {ref_depth_value}")
    print(f"Reference distance: {ref_distance}")

    # 선형 맵핑을 위한 비율 계산
    ratio = ref_distance / (ref_depth_value - max_depth_value)  # 깊이 값 범위

    # 깊이 맵을 절대 거리로 변환
    absolute_distances = np.abs(((max_depth_value - depth_map) * ratio))**3

    return absolute_distances

def visualize_and_save_depth_map(absolute_distances, output_file):
    plt.imshow(absolute_distances, cmap='plasma', origin='lower')
    plt.colorbar(label='Distance (meters)')
    plt.title('Absolute Distance Map')
    plt.xlabel('X-axis (pixels)')
    plt.ylabel('Y-axis (pixels)')

    # 시각화 결과 저장
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()

def get_latest_pfm(pfm_folder_path):
    # PFM 폴더에서 가장 최근에 생성된 PFM 파일 찾기
    pfm_files = glob.glob(os.path.join(pfm_folder_path, '*.pfm'))
    if not pfm_files:
        print(f"PFM 파일을 찾을 수 없습니다: {pfm_folder_path}")
        exit(1)

    latest_pfm_file = max(pfm_files, key=os.path.getctime)  # 가장 최근에 수정된 파일
    print(f"가장 최근에 생성된 PFM 파일: {latest_pfm_file}")

    return latest_pfm_file

def get_ref_point_from_txt(txt_folder_path):
    # txt 폴더에서 좌표를 찾는 함수
    txt_files = glob.glob(os.path.join(txt_folder_path, '*.txt'))
    if not txt_files:
        print("5미터 지점 찾기 실패")
        return None

    latest_txt_file = max(txt_files, key=os.path.getctime)
    print(f"가장 최근에 생성된 TXT 파일: {latest_txt_file}")

    with open(latest_txt_file, 'r') as file:
        line = file.readline().strip()
        if "5m point at" in line:
            # "5m point at (x, y)" 형식에서 좌표를 추출
            coords = line.split("at")[1].strip(" ()\n").split(",")
            ref_point = (int(coords[0]), int(coords[1]))
            return ref_point
        else:
            print("TXT 파일에서 좌표를 읽을 수 없습니다.")
            return None

# 참조 거리 설정
reference_distance = 1.7  # 참조 지점의 실제 거리 1.7**3 (미터)

# PFM 파일이 있는 폴더 경로
pfm_folder_path = './output_monodepth/'  # PFM 파일이 저장된 폴더 경로

# TXT 파일이 있는 폴더 경로
txt_folder_path = './recording/images/'  # TXT 파일이 저장된 폴더 경로

# 결과 이미지 저장 경로
output_image_path = './distance_specify_result/roadview3.png'  # 저장할 이미지 파일 이름과 경로

# 가장 최근에 생성된 PFM 파일 찾기
pfm_file_path = get_latest_pfm(pfm_folder_path)

# 가장 최근에 생성된 TXT 파일에서 참조 지점 찾기
ref_point = get_ref_point_from_txt(txt_folder_path)

if ref_point is not None:
    # 절대 거리 계산
    absolute_distances = calculate_absolute_distance(pfm_file_path, ref_point, reference_distance)

    # 결과 시각화 및 저장
    visualize_and_save_depth_map(absolute_distances, output_image_path)
