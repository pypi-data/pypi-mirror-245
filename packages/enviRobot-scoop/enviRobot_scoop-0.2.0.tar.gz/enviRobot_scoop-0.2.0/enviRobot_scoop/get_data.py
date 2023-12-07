from geopy import Point
from geopy.distance import distance, geodesic
import requests
import datetime as dt
from .plotly_screenshot import save_fig

def get_square_bounds(center_lat, center_lon, distance_in_km):
    # 設定中心點
    center = Point(center_lat, center_lon)

    # 計算經度和緯度的偏移量
    lat_offset = distance(kilometers=distance_in_km).destination(
        center, bearing=0).latitude - center_lat
    lon_offset = distance(kilometers=distance_in_km).destination(
        center, bearing=90).longitude - center_lon

    # 計算正方形範圍的左上和右下角經緯度
    top_left_lat = round(center_lat + lat_offset, 4)
    top_left_lon = round(center_lon - lon_offset, 4)
    bottom_right_lat = round(center_lat - lat_offset, 4)
    bottom_right_lon = round(center_lon + lon_offset, 4)

    return (top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)


# 這最好是INT啦xDDD
def get_aiot_rawdata(int_lat, int_lon, str_datetime, image_name, lang='CH'):
    if lang not in ['EN', 'CH']:
        raise ValueError('supported language: CH, EN')
    date_now = dt.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
    date_five_minutes_ago = date_now - dt.timedelta(minutes=5)
    str_five_minutes_ago = date_five_minutes_ago.strftime("%Y-%m-%d %H:%M:%S")
    # print(int_lat, int_lon, str_datetime, str_five_minutes_ago, flush=True)
    top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon = get_square_bounds(
        int_lat, int_lon, 1)
    # print(top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon, flush=True)
    aiot_rawdata_api = f"https://aiot.moenv.gov.tw/_/api/v2/iot/rawdata?fields=pm2_5&" \
    f"start_time={str_five_minutes_ago}&end_time={str_datetime}&min_lat={bottom_right_lat}&max_lat={top_left_lat}&" \
    f"min_lon={top_left_lon}&max_lon={bottom_right_lon}&resample=5min&return_format=json"
    # print("[gpt / get_aiot_rawdata]", aiot_rawdata_api, flush=True)

    try:
        res = requests.get(aiot_rawdata_api)
        if res.status_code != 200:
            print("[gpt / get_aiot_rawdata] load api fail\n", aiot_rawdata_api, flush=True)
            output = ""
        list_result = res.json()["data"]
        if len(list_result) == 0:
            print("[gpt / get_aiot_rawdata] load api empty\n", aiot_rawdata_api, flush=True)
            output = ""
        if lang == 'EN':
            output = "PM2.5 sensor concentrations within a one-kilometer square: \n"
        elif lang == 'CH':
            output = "以下為一公里方形內的 IoT pm2_5感測器濃度：\n"
        deviceIds = set()

        for item in reversed(list_result):
            deviceId = item["deviceId"]
            if deviceId not in deviceIds:
                deviceIds.add(deviceId)
                lat, lon = item["lat"], item["lon"]
                pm2_5 = item["pm2_5"]
                output += f"[{deviceId}] [{lat:.4f}, {lon:.4f}] , {pm2_5:.2f}\n"

        if not deviceIds:
            if lang == 'EN':
                output += "No sensor data"
            elif lang == 'CH':
                output += "無pm2_5感測器資料"
            return output

    except:
        if lang == 'CH':
            output = "連接aiot rawdata時出錯"
        elif lang == 'EN':
            output = "An error occured while processing aiot rawdata"
    sensor_map_url = 'https://aiot.moenv.gov.tw/web/iot/history/animation?'+\
            f'start={(date_now-dt.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")}&'+\
            f'end={(date_now+dt.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")}&'+\
            f'start_lat={bottom_right_lat:.4f}&end_lat={top_left_lat:.4f}&start_lon={top_left_lon:.4f}&end_lon={bottom_right_lon:.4f}'
    print('get_aiot_rawdata/take screenshot start', flush=True)
    #aiot_screenshot(sensor_map_url, f'./image/{image_name}.png')
    save_fig(int_lat, int_lon, list_result, f'./image/{image_name}.png')
    print('get_aiot_rawdata/take screenshot finish', flush=True)
    if lang == 'EN':
        output += f"\n\nPM2.5 sensor map link: {sensor_map_url.replace(' ','%20')}"
    elif lang == 'CH':
        output += f"\n\nPM2.5 感測器地圖URL : {sensor_map_url.replace(' ','%20')}"
    # print('aiot api done', flush=True)
    return output

def get_cwb_wind_data(int_lat, int_lon, str_datetime, lang='CH'):
    if lang not in ['EN', 'CH']:
        raise ValueError('supported language: CH, EN')
    event_loc = (int_lat, int_lon)
    event_time = dt.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
    # 後一個整點? API有問題, start_time要往後8小時
    # 修好了
    #t = (event_time+dt.timedelta(hours=9, minutes=-event_time.minute, seconds=-event_time.second))
    t = (event_time+dt.timedelta(minutes=-event_time.minute, seconds=-event_time.second))
    str_result = "No CWB sensor data" if lang=="EN" else "無氣象局測站資料"
    for _ in range(3):
        start_time, end_time = t.strftime("%Y-%m-%d %H:%M:%S"), (t+dt.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        t = t - dt.timedelta(hours=1)
        # print(int_lat, int_lon, str_datetime, str_five_minutes_ago, flush=True)
        cwb_api = f'https://aiot.moenv.gov.tw/_/api/v2/epa_station/wind?fields=wind_direct%2Cwind_speed&sources=中央氣象局&min_lat=-90&max_lat=90&min_lon=-180&max_lon=180&start_time={start_time}&end_time={end_time}'
        # print(cwb_api, flush=True)
        response = requests.get(cwb_api)
        j = response.json()
        if len(j['data']) != 0:
            nearest_site, nearest_dist = None, None
            for i in range(len(j['data'])):
                site_loc = (j['data'][i]['lat'],j['data'][i]['lon'])
                dist = geodesic(event_loc, site_loc).km
                if nearest_dist is None or dist < nearest_dist:
                    nearest_site, nearest_dist = j['data'][i], dist
            #print(nearest_site, flush=True)
            #print(nearest_site['lat'],nearest_site['lon'], flush=True)
            if lang == 'EN':
                str_result = f"Closest meteorological station data: \nStation: {nearest_site['name']}({nearest_dist:.2f} km away)\nData time: {nearest_site['time']}\nWind direction: {nearest_site['wind_direct']}\nWind speed: {nearest_site['wind_speed']}"
            elif lang == 'CH':
                str_result = f"以下為距離最近的氣象局測站資料:\n測站: {nearest_site['name']}(距離{nearest_dist:.2f}公里)\n資料時間: {nearest_site['time']}\n風向: {nearest_site['wind_direct']}\n風速: {nearest_site['wind_speed']}"
            break
        else:
            #print('continue', flush=True)
            continue
    return str_result