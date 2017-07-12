#coding:utf8
import numpy as np
import math
import urllib
import json





def bd_decrypt(bd_lat, bd_lon):
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = np.sqrt(x * x + y * y) - 0.00002 * np.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * np.cos(x * x_pi)
    gg_lon = z * np.cos(theta)
    gg_lat = z * np.sin(theta)
    return gg_lat, gg_lon


def baidu2gaode_api(bd_lat, bd_lng):
    gaode_api_key='21de06058cddabad87a6b505e207e979'
    url="http://restapi.amap.com/v3/assistant/coordinate/convert?locations=%lf,%lf&coordsys=baidu&output=json&key=%s"%(bd_lng, bd_lat, gaode_api_key)
    print url
    response = urllib.urlopen(url)
    s = response.read()
    info = json.loads(s)
    items = info['locations'].split(',')
    lng = float(items[0])
    lat = float(items[1])
    return lat, lng


if __name__=='__main__':
    baidu2gaode_api(40.0406120000,116.3179170000)
