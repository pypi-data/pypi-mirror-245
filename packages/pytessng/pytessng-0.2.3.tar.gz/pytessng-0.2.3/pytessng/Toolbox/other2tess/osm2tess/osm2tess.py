from .utils.my_class import OSMData, Network, NetworkCreator


def osm2tess(netiface, params):
    # params:
    # - lon_0
    # - lat_0
    # - length

    lon_0 = params["lon_0"]
    lat_0 = params["lat_0"]
    distance = params["distance"]

    # bounding_box = {
    #     "lon_min": 113.80543,
    #     "lon_max": 114.34284,
    #     "lat_min": 29.69543,
    #     "lat_max": 31.84852,
    # }
    center_point = {
        "lon_0": lon_0,
        "lat_0": lat_0,
        "distance": distance,
    }
    # osm_file_path = "nanjing.osm"

    params = {
        "osm_file_path": None,
        "bounding_box": None,
        "center_point": center_point,
        "road_type": ["高速公路", "城市道路"],
        "projection": None,
    }
    name = f"{lon_0}-{lat_0}-{distance}"
    osm_data = OSMData(params).get_osm_data(name)
    
    network = Network(**osm_data)
    # network.draw()
    
    network_creator = NetworkCreator(netiface, network)
    
    return network_creator.error_message

