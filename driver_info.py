#!/usr/bin/python
#coding:utf8
import re
import simplekml
import json
import utils
oid_re=re.compile("\d+")
class Analyzer:
    def __init__(self):
        self.kml = simplekml.Kml()
        pass

    def creat_multiGeometry(self, Oid):
        tmp = "Oid:"+Oid
        self.multigeo = self.kml.newmultigeometry(name=tmp)
        pass

    def load_driver_info(self, data):
        for order in data['order_info']:
            self.multigeo.newlinestring(coords=[(order['flng'], order['flat']), (order['tlng'], order['tlat'])])
            self.multigeo.newpoint(coords=[(order['flng'], order['flat'])])


    def load_order_info(self, data):
        if type(data) == dict:
            self.multigeo.newlinestring(coords=[(data['flng'], data['flat']), (data['tlng'], data['tlat'])])
            self.multigeo.newpoint(coords=[(data['flng'], data['flat'])])

    def load_driver_loc_info(self, line):
        items = line.split(";")
        lat = float(items[1].replace("d:",""))
        lng = float(items[3].replace("d:",""))
        dlat, dlng = utils.baidu2gaode_api(lat, lng)
        self.multigeo.newpoint(coords=[(dlng, dlat)])

    def write_kml(self, outfn):
        self.kml.save(outfn)


if __name__ == "__main__":
    worker = Analyzer()
    case_name = "MultiGeometry"

    Ofile = open("orderId")
    Dfile = open("driverId")

    per_num = 10

    count = 0
    while 1:
        count += 1
        oid = Ofile.readline()
        did = Dfile.readline()
        result=oid_re.findall(oid)
        if len(result) == 0:
            break
        oid=result[0]
        result=oid_re.findall(did)
        did=result[0]

        worker.creat_multiGeometry(oid)

        djsonfile = open("drivers.json.stability")
        while 1:
            line = djsonfile.readline()
            if not line:
                break
            line = line.replace(" ", "")
            data = json.loads(line)
            if str(data["driverId"]) == str(did):
                worker.load_driver_info(data)
                break

        ojsonfile = open("orders.json.stability")
        while 1:
            line = ojsonfile.readline()
            if not line:
                break
            line = line.replace(" ", "")
            data = json.loads(line)
            if str(data["orderId"]) == str(oid):
                worker.load_order_info(data)
                break

        dlocfile = open("d_loc.json.stability")
        while 1:
            line = dlocfile.readline()
            if not line:
                break
            line = line.strip().replace(" ", "")
            items = line.split("_")
            tmp_line = items[2]
            items = tmp_line.split("|")
            loc_oid = items[0]
            if str(loc_oid) == str(oid):
                worker.load_order_info(line)
                break

        if count%per_num == 0:
            worker.write_kml("../" + case_name + str(count/per_num)+ ".kml")
            worker = Analyzer()