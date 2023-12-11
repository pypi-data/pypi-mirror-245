if __name__ == "__main__":
    from excel2tess import excel2tess
    from opendrive2tess import opendrive2tess
    from shape2tess import shape2tess
    from osm2tess import osm2tess
else:
    from .excel2tess import excel2tess
    from .opendrive2tess import opendrive2tess
    from .shape2tess import shape2tess
    from .osm2tess import osm2tess


def other2tess(netiface, params, mode):
    print(f"Import mode: {mode}.")

    if mode == "excel":
        error_message = excel2tess.excel2tess(netiface, params)
    elif mode == "opendrive":
        error_message = opendrive2tess.opendrive2tess(netiface, params)
    elif mode == "shape":
        error_message = shape2tess.shape2tess(netiface, params)
    elif mode == "osm":
        error_message = osm2tess.osm2tess(netiface, params)
    else:
        raise Exception("No this import mode !")

    return error_message

