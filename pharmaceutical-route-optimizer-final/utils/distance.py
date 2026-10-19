import math
def calculate_distance(point1,point2):
 x1,y1=point1; x2,y2=point2; return math.sqrt((x2-x1)**2+(y2-y1)**2)
def get_location(chemist): return (chemist["x"],chemist["y"])
def calculate_route_distance(route,warehouse,chemists):
 lookup={c["id"]:get_location(c) for c in chemists}; current=(warehouse["x"],warehouse["y"]); total=0
 for cid in route: total+=calculate_distance(current,lookup[cid]); current=lookup[cid]
 if route: total+=calculate_distance(current,(warehouse["x"],warehouse["y"]))
 return total
