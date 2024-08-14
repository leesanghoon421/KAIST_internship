import numpy as np
import matplotlib.pyplot as plt

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

def calculate_absolute_distance(pfm_path, ref_distance):
    depth_map, scale = load_pfm(pfm_path)
    height, width = depth_map.shape[:2]

    # 참조 지점의 x좌표는 이미지의 중심, y좌표는 최대 y의 8분의 1
    ref_point = (width // 2, height // 8)

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

# 참조 거리 설정
reference_distance = 1.7  # 참조 지점의 실제 거리 1.7**3 (미터)

# PFM 파일 경로
pfm_file_path = './output_monodepth/tester2.pfm'  # 여기에 PFM 파일 경로를 입력하세요.

# 결과 이미지 저장 경로
output_image_path = './distance_result/tester2.png'  # 저장할 이미지 파일 이름과 경로

# 절대 거리 계산
absolute_distances = calculate_absolute_distance(pfm_file_path, reference_distance)

# 결과 시각화 및 저장
visualize_and_save_depth_map(absolute_distances, output_image_path)
