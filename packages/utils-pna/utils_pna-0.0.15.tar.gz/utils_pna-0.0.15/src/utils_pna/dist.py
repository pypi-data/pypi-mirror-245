from math import radians, cos, sin, asin, sqrt

def compute_haversine(lon1, lat1, lon2, lat2, conv=1):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r * conv

def haversine(unidad="km", **args):
    conv = 1 if unidad == "km" else 1 / 1.852

    if len(args) == 2:
        if isinstance(args[0], list):
            return compute_haversine(args[0][0], args[0][1], args[1][0], args[1][1], conv=conv)
        else:
            return compute_haversine(args[0].x, args[0].y, args[1].x, args[1].y, conv=conv)
    elif len(args) == 4:
        return compute_haversine(args[0], args[1], args[2], args[3], conv=conv)
    else:
        raise ValueError(f"Tamaño 2 o 4 esperado, obtenido: {len(args)}")
    
def distancia_linea(punto, linestring):
    punto_cercano = linestring.interpolate(linestring.project(punto))

    return haversine(
        punto, punto_cercano
    )