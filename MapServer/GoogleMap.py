import requests

def get_nearby_places(address, place_type):
    api_key = '<your_api_key>'
    geocoding_endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'
    places_endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    # 获取地址的经纬度坐标
    geocoding_params = {
        'address': address,
        'key': api_key
    }

    geocoding_response = requests.get(geocoding_endpoint, params=geocoding_params)
    geocoding_data = geocoding_response.json()

    if geocoding_data['status'] == 'OK':
        location = geocoding_data['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']

        # 在给定坐标附近搜索指定类型的地点
        places_params = {
            'location': f'{lat},{lng}',
            'radius': 1000,  # 搜索半径（单位：米）
            'type': place_type,
            'key': api_key
        }

        places_response = requests.get(places_endpoint, params=places_params)
        places_data = places_response.json()

        if places_data['status'] == 'OK':
            places = places_data['results']
            for place in places:
                name = place['name']
                address = place['vicinity']
                print(f"Name: {name}\nAddress: {address}\n")
        else:
            print('Error occurred while searching for places.')
    else:
        print('Error occurred while geocoding the address.')


# 使用示例
address = '123 Main Street, City, Country'  # 替换为你的地址
place_type = 'school'  # 替换为你要搜索的地点类型（例如：restaurant）

get_nearby_places(address, place_type)
