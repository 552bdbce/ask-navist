import urllib.request
import json
import urllib.parse
from datetime import datetime, timezone, timedelta
import isodate

#Google Maps Platform Directions API endpoint
f = open('private.txt', 'r')
datalist = f.readlines()
endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = datalist[0]

naist = '34.73342950684778, 135.73205690071669'
home = datalist[1]

# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')


class Gmaps:
    def __init__(self):
        print("gmaps")
        self.direction = None
        self.time = None
        self.duration = None

    def get_dep_time(self):
        jst_time = datetime.now(JST)
        if self.time is not None:
            TimeHMS = self.time.split(':')
            dep_time_jst = jst_time.replace(hour=int(TimeHMS[0]), minute=int(TimeHMS[1]))
            if dep_time_jst.timestamp() < jst_time.timestamp():
                dep_time_jst = dep_time_jst + timedelta(days=1)
            self.dep_time = int(dep_time_jst.timestamp())
        elif self.duration is not None:
            dep_time_jst = jst_time + isodate.parse_duration(self.duration)
            if dep_time_jst.timestamp() < jst_time.timestamp():
                dep_time_jst = dep_time_jst + timedelta(days=1)
            self.dep_time = int(dep_time_jst.timestamp())
        else:
            self.dep_time = 'now'

    def set_coordinate(self):
        if self.direction == 'ToSchool':

            self.origin = home
            self.destination = naist
        else:
            self.origin = naist
            self.destination = home

    def get_json(self):
        nav_request = 'language=ja&origin={}&destination={}&departure_time={}&key={}'.format(self.origin, self.destination,
                                                                                             self.dep_time, api_key)
        nav_request = urllib.parse.quote_plus(nav_request, safe='=&')
        request = endpoint + nav_request
        print(request)

        # Google Maps Platform Directions APIを実行
        response = urllib.request.urlopen(request).read()

        # 結果(JSON)を取得
        directions = json.loads(response)
        data = json.loads(response.decode('utf-8'))
        # print("出発時間は", datetime.fromtimestamp(self.dep_time))
        routes_string = ''
        for key in data['routes']:
            # print(key) # titleのみ参照
            # print(key['legs'])
            for key2 in key['legs']:
                # print(key2['distance']['text'])
                # print(key2['duration_in_traffic']['text'])
                for key3 in key2['steps']:
                    # print(key3['html_instructions'])
                    routes_string += key3['html_instructions']

        if all(map(routes_string.__contains__, ('国道168号', 'けやき通り', '国道163号'))):
            routes = 'A'
        elif all(map(routes_string.__contains__, ('国道168号', 'ならやま大通り', '国道163号'))):
            routes = 'B'
        elif all(map(routes_string.__contains__, ('国道168号', '国道163号'))):
            routes = 'C'
        else:
            routes = 'unknown'

        if self.dep_time != 'now':
            return routes, key2['duration_in_traffic']['text'], datetime.fromtimestamp(self.dep_time).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return routes, key2['duration_in_traffic']['text'], self.dep_time

test = Gmaps()
test.direction = 'ToHome'
# test.time = '10:00'
test.duration = 'PT10M'
test.set_coordinate()
test.get_dep_time()
print(test.get_json())

