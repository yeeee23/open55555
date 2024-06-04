# 지역을 입력받아서 좌표를 뽑고 그 좌표로 날씨를 요청하여 받는 코드 

import pandas as pd
import requests
import datetime

# CSV 파일을 읽어옵니다.
xy_df = pd.read_csv("/Users/yang-yeeun/Downloads/location_file.csv")

# NaN 값을 0으로 대체합니다.
a_df = xy_df.fillna(0)

# 사용자 입력을 받습니다.
input_1단계 = input("1단계 값을 입력하세요: ")
input_2단계 = input("2단계 값을 입력하세요: ")
input_3단계 = input("3단계 값을 입력하세요 (값이 없으면 Enter를 누르세요): ")

# 필터링 조건을 확인합니다.
print(f"Filtering with: 1단계={input_1단계}, 2단계={input_2단계}, 3단계={input_3단계}")

# 입력된 값과 데이터프레임의 값이 일치하는 행을 필터링합니다.
filtered_df = a_df[(a_df['1단계'] == input_1단계) & (a_df['2단계'] == input_2단계) & (a_df['3단계'] == input_3단계)]

# 필터링된 결과를 출력합니다.
if not filtered_df.empty:
    # 사용자가 입력한 값과 매칭되는 좌표를 가져옵니다.
    nx = filtered_df.iloc[0]['격자 X']
    ny = filtered_df.iloc[0]['격자 Y']

    # API 설정
    API_Key = "GnN6ZfisAdn3qQa34ktd+Z+++jaBYfhYjNgg7h3tlIwDdm+3H2MxKqDJrN9QC6WC4kQoC8yckS3Qgwm9CqzoSQ=="
    URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"

    # 현재 시간 설정
    today = datetime.datetime.today()
    base_date = today.strftime("%Y%m%d")
    base_time = "0800"

    # API 요청 파라미터 설정
    params = {
        "serviceKey": API_Key,
        "dataType": "json",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
        "numOfRows": 10,
        "pageNo": 1
    }

    # API 호출
    res = requests.get(URL, params=params)
    items = res.json().get('response').get('body').get('items')

    # 날씨 정보 추출
    weather_data = dict()
    for item in items['item']:
        if item['category'] == 'TMP':
            weather_data['tmp'] = item['fcstValue']
        if item['category'] == 'PTY':
            weather_code = item['fcstValue']
            if weather_code == '1':
                weather_state = '비'
            elif weather_code == '2':
                weather_state = '비/눈'
            elif weather_code == '3':
                weather_state = '눈'
            elif weather_code == '4':
                weather_state = '소나기'
            else:
                weather_state = '없음'
            weather_data['code'] = weather_code
            weather_data['state'] = weather_state

    # 날씨 정보 출력
    print(f"격자 좌표 ({nx}, {ny})의 오늘 기온:", weather_data.get('tmp', '정보 없음'), "도")
    print(f"격자 좌표 ({nx}, {ny})의 오늘 날씨 상태:", weather_data.get('state', '정보 없음'))
else:
    print("입력된 지역에 대한 정보가 없습니다.")
