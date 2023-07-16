from static.Scheduling import scheduling
import json
travel_planner = scheduling("Beijing", "Singapore", 3, "2023-7-26")

s = json.loads(travel_planner.toJSON())
print(s)
