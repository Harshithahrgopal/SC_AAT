import copy
from algorithm.evolutionary_algorithm import run_evolutionary_algorithm
def create_test_cases(chemists,vehicles):
 normal=copy.deepcopy(chemists); low=copy.deepcopy(chemists); high=copy.deepcopy(chemists); tight=copy.deepcopy(chemists); loc=copy.deepcopy(chemists)
 for c in low:c["demand"]=max(1,c["demand"]//2)
 for c in high:c["demand"]*=2
 for i,c in enumerate(tight):
  s=9+(i%3); c["time_window"]=(s,s+1)
 for i,c in enumerate(loc): c["x"]+=(i%3)-1; c["y"]+=((i+1)%3)-1
 return [("Normal Case","Original input",normal),("Low Demand","Demand approximately halved",low),("High Demand","Demand doubled",high),("Tight Time Windows","One-hour windows",tight),("Changed Locations","Coordinates changed slightly",loc)]
def run_test_cases(warehouse,vehicles,chemists,population_size=50,generations=100,mutation_rate=0.1,crossover_rate=0.8,tournament_size=3):
 out=[]
 for name,desc,case in create_test_cases(chemists,vehicles):
  r=run_evolutionary_algorithm(chemists=case,vehicles=vehicles,warehouse=warehouse,population_size=population_size,generations=generations,mutation_rate=mutation_rate,crossover_rate=crossover_rate,tournament_size=tournament_size); b=r["best_result"]; out.append({"Test Case":name,"Description":desc,"Total Distance":b["total_distance"],"Fitness":b["fitness"],"Capacity Violation":b["capacity_violation"],"Late Minutes":b["late_minutes"]})
 return out
