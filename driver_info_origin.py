#!/usr/bin/python
#coding:utf8

import simplekml
import json
import utils

class Analyzer:
    def __init__(self):
        self.kml = simplekml.Kml()
        pass

    def load_driver_info(self, fn):
        with open(fn) as fid:
            line = fid.readline()
            line = line.replace(" ","")
            data = json.loads(line)
            for order in data['order_info']:
                self.kml.newlinestring(name="order_on_car", description="order_on_car",
                                  coords=[(order['flng'], order['flat']), (order['tlng'], order['tlat'])])
                self.kml.newpoint(name="on_car_order_origin", coords=[(order['flng'], order['flat'])])


    def load_order_info(self, fn):
        with open(fn) as fid:
            line = fid.readline()
            line = line.replace(" ","")
            data = json.loads(line)
            if type(data) == dict:
                lin = self.kml.newlinestring(name="new_order", description="new_order",
                                       coords=[(data['flng'], data['flat']), (data['tlng'], data['tlat'])])
                lin.style.linestyle.color = simplekml.Color.darkgreen
                self.kml.newpoint(name="order_origin", coords=[(data['flng'], data['flat'])])

    def load_driver_loc_info(self, fn):
        with open(fn) as fid:
            for line in fid.readlines():
                line = line.strip().replace(" ", "")
                items = line.split(";")
                lat = float(items[1].replace("d:",""))
                lng = float(items[3].replace("d:",""))
                dlat, dlng = utils.baidu2gaode_api(lat, lng)
                self.kml.newpoint(name="driver_loc", coords=[(dlng, dlat)])


                
    def write_kml(self, outfn):
        self.kml.save(outfn)


if __name__ == "__main__":
    worker = Analyzer()
    case_name = "test"
    worker.load_driver_info("/Users/gongyuanfeng/DiDiWork/single case/crm/drivers.json.stability")
    worker.load_order_info("/Users/gongyuanfeng/DiDiWork/single case/crm/orders.json.stability")
    worker.load_driver_loc_info("/Users/gongyuanfeng/DiDiWork/single case/crm/d_loc.json.stability")
    worker.write_kml("../"+case_name+".kml")

