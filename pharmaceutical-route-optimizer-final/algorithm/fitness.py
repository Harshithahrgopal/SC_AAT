from utils.distance import calculate_distance
TRAVEL_TIME_PER_DISTANCE=10
CAPACITY_PENALTY=1000
TIME_PENALTY=10
def create_chemist_lookup(chemists): return {c["id"]:c for c in chemists}
def calculate_capacity_penalty(route,lookup,capacity):
 load=sum(lookup[c]["demand"] for c in route); excess=max(0,load-capacity); return excess*CAPACITY_PENALTY,load,excess
def calculate_time_penalty(route,warehouse,lookup):
 current=(warehouse["x"],warehouse["y"]); t=8*60; penalty=0; late_total=0; arrivals=[]
 for cid in route:
  c=lookup[cid]; nxt=(c["x"],c["y"]); t+=calculate_distance(current,nxt)*TRAVEL_TIME_PER_DISTANCE; earliest=c["time_window"][0]*60; latest=c["time_window"][1]*60
  if t<earliest: t=earliest
  late=max(0,t-latest); late_total+=late; penalty+=late*TIME_PENALTY; arrivals.append({"chemist":cid,"arrival_time":t,"late_minutes":late}); current=nxt
 return penalty,late_total,arrivals
def calculate_solution_distance(solution,warehouse,chemists):
 lookup=create_chemist_lookup(chemists); wh=(warehouse["x"],warehouse["y"]); total=0
 for route in solution:
  if not route: continue
  current=wh
  for cid in route:
   nxt=(lookup[cid]["x"],lookup[cid]["y"]); total+=calculate_distance(current,nxt); current=nxt
  total+=calculate_distance(current,wh)
 return total
def calculate_fitness(solution,warehouse,vehicles,chemists):
 lookup=create_chemist_lookup(chemists); distance=calculate_solution_distance(solution,warehouse,chemists); cap_pen=time_pen=cap_violation=late_total=0; details=[]
 for i,route in enumerate(solution):
  cp,load,excess=calculate_capacity_penalty(route,lookup,vehicles[i]["capacity"]); tp,late,arrivals=calculate_time_penalty(route,warehouse,lookup); cap_pen+=cp; time_pen+=tp; cap_violation+=excess; late_total+=late; details.append({"vehicle":vehicles[i]["id"],"route":route,"load":load,"capacity":vehicles[i]["capacity"],"capacity_excess":excess,"late_minutes":late,"arrivals":arrivals})
 return {"fitness":distance+cap_pen+time_pen,"total_distance":distance,"capacity_penalty":cap_pen,"time_penalty":time_pen,"capacity_violation":cap_violation,"late_minutes":late_total,"route_details":details}
