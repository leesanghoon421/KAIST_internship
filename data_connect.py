import subprocess
import ast
import requests
from geopy.distance import geodesic

# gps_est.py 스크립트를 실행하고 출력을 캡처
print("Running gps_est.py to get estimated GPS coordinates...\n")
result = subprocess.run(["python3", "gps_est.py"], capture_output=True, text=True)

# 출력된 내용을 문자열로 가져옴
output = result.stdout
print("Captured output from gps_est.py:\n", output)

# 출력 내용에서 GPS 좌표 부분만 추출
lines = output.splitlines()
gps_coordinates = []
responses = []

print("\nExtracting GPS coordinates from output...")
for line in lines:
    if "예측 GPS 좌표" in line:
        # 좌표 부분만 추출
        start_idx = line.find(": (") + 3  # ": (" 다음부터 시작
        end_idx = line.find(")", start_idx)
        coordinate_str = line[start_idx:end_idx]
        gps_coordinate = ast.literal_eval(coordinate_str)
        gps_coordinates.append(gps_coordinate)
        print(f"Extracted GPS coordinate: {gps_coordinate}")

# API 엔드포인트 (좌표로 도로명 주소 조회)
coordinate_url = "https://gs1geo.oliot.kr/api/address"

print("\nSending API requests to get road names...")
# 모든 추출된 좌표에 대해 API 요청 보내기
for idx, gps_coordinate in enumerate(gps_coordinates):
    # 위도와 경도를 그대로 사용
    latitude = gps_coordinate[0]
    longitude = gps_coordinate[1]

    # 좌표를 문자열로 변환
    coordinate_str = f"{latitude}, {longitude}"

    # 파라미터 설정
    params = {
        'coordinate': coordinate_str
    }

    # GET 요청 보내기
    response = requests.get(coordinate_url, params=params)

    # 응답 상태 코드 확인 및 응답 데이터 저장
    if response.status_code == 200:
        # 응답 JSON 데이터 가져오기
        data = response.json()
        if data['status']:
            responses.append({
                "index": idx + 1,
                "gps_coordinate": gps_coordinate,
                "road_name": data['data']['road_name'],
                "raw_data": data
            })
            print(f"Received road name '{data['data']['road_name']}' for coordinate {gps_coordinate}")
        else:
            print(f"Failed to get road name for coordinate {gps_coordinate}")
    else:
        print(f"API request failed for coordinate {gps_coordinate} with status code {response.status_code}")

# 동일한 도로명 주소에 대한 응답 그룹화
road_name_groups = {}
print("\nGrouping responses by road name...")
for response in responses:
    road_name = response['road_name']
    if road_name not in road_name_groups:
        road_name_groups[road_name] = []
    road_name_groups[road_name].append(response)
    print(f"Grouped coordinate {response['gps_coordinate']} under road name '{road_name}'")

# 결과 리스트에 대해 최종 필터링
final_results = []
print("\nFiltering results to keep the closest coordinates for duplicated road names...")
for road_name, grouped_responses in road_name_groups.items():
    if len(grouped_responses) > 1:
        print(f"\nProcessing duplicated road name '{road_name}' with {len(grouped_responses)} coordinates...")
        # 도로명 주소에 대한 정확한 좌표를 가져오기 위해 API 호출
        road_name_url = "https://gs1geo.oliot.kr/api/address"
        road_name_params = {'roadName': road_name}
        correct_coord_response = requests.get(road_name_url, params=road_name_params)

        if correct_coord_response.status_code == 200:
            correct_data = correct_coord_response.json()
            if correct_data['status']:
                correct_coord = correct_data['data']['coordinate']
                print(f"Correct coordinate for road name '{road_name}': {correct_coord}")
                min_distance = float('inf')
                closest_response = None
                for response in grouped_responses:
                    estimated_coord = response['gps_coordinate']
                    distance = geodesic(estimated_coord, correct_coord).meters
                    print(f"Distance from {estimated_coord} to correct coordinate: {distance:.2f} meters")
                    if distance < min_distance:
                        min_distance = distance
                        closest_response = response
                        print(f"New closest coordinate found: {estimated_coord} with distance {min_distance:.2f} meters")
                # 모든 그룹의 가장 가까운 좌표를 결과에 추가
                final_results.append(closest_response)
            else:
                print(f"Failed to get correct coordinate for road name '{road_name}' - API status was False")
        else:
            print(f"Failed to get correct coordinate for road name '{road_name}' with status code {correct_coord_response.status_code}")
    else:
        # 중복되지 않는 경우 그대로 결과에 추가
        final_results.extend(grouped_responses)

# 최종 결과 출력
print("\nFinal results:")
for result in final_results:
    print(f"Final GPS coordinate {result['index']}: Estimated - {result['gps_coordinate']}, Road Name - {result['road_name']}, Full Response - {result['raw_data']}")