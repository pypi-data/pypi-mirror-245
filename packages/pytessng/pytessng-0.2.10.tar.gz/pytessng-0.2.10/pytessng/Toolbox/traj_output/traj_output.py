import time
import math


def get_traj_data(simuiface, proj, p2m):
    # 当前已仿真时间，单位：毫秒
    simuTime = simuiface.simuTimeIntervalWithAcceMutiples()

    # 当前正在运行车辆列表
    lAllVehi = simuiface.allVehiStarted()
    
    traj_data = {
        "timestamp": str(int(time.time() * 1000)),
        'start_sim_time': simuiface.startMSecsSinceEpoch(),
        "simu_time": simuTime,
        "count": len(lAllVehi),
        "objs": [],
    }
    
    for vehi in lAllVehi:
        x = p2m(vehi.pos().x())
        y = -p2m(vehi.pos().y())
        if math.isnan(x) or math.isnan(y):
            continue
        
        euler = vehi.vehicleDriving().euler()
        in_link = vehi.roadIsLink()
        lane = vehi.lane()
        
        veh_data = {
            "id": vehi.id(),
            'roadId': vehi.roadId(),
            'inLink': in_link,
            'laneCount': in_link and lane.link().laneCount(),
            'laneNumber': in_link and lane.number(),
            'laneTypeName': in_link and lane.actionType(),
            'typeCode': vehi.vehicleTypeCode(),
            'angle': vehi.angle(),
            'speed': p2m(vehi.currSpeed()),
            'size': [vehi.length(), 2, 2],
            'color': "",
            'x': x,
            'y': y,
            'z': vehi.v3z(),
            'longitude': None,
            'latitude': None,
            'eulerX': euler.x(),
            'eulerZ': euler.y(),
            'eulerY': euler.z(),
        }

        # 是否有经纬度
        if proj:
            lon, lat = proj(x, y, inverse=True)
            veh_data['longitude'] = lon
            veh_data['latitude'] = lat
    
        traj_data['objs'].append(veh_data)

    return traj_data

