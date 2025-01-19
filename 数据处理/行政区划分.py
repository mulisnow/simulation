import json

def load_geo_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def is_point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


geo_data = load_geo_data("C:/Users/Herzog\Desktop/2025美赛/数据/城市2行政区经纬度/回民县.json")
coordinates = geo_data['geometry']['coordinates'][0]


point_to_check = (111.600365, 40.929106)
is_inside = is_point_in_polygon(point_to_check, coordinates)

print(f"点 {point_to_check} 在多边形内: {is_inside}")