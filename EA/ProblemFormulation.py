"""
This file try to model the problem of "travel planning and hotel selection" and use Evolutionary Algorithm to solve it!
Vertexes are classified into two types: 'Attraction' and 'Hotel'
We need to decide which hotel to start and end with.
Every day, we depart from one 'Hotel' we choose and visit all the scheduled 'Attractions' in some order.
In our algorithm, we need to decide which "Hotel" we live, which attractions are visited in which day, what is the order to visit all the attractions in one day.
$Optimization Objects:
-->1. Minimum of travel Time in the road(without visiting)
-->2. Minimum of Cost, consisting of lodging expenses and travel expenses.
$Constraints:
-->1. Time Window: Each attraction has its best visiting time
-->2. One day can only have 14 hours to travel

Vertexes:
    Attraction:
        Attributes: [referTime(estimated time to visit this attraction), timeWindow(best time for visiting)

    Hotel:
        Attributes: [expenses(cost per day)]

Edges:
    Subway_Time_Table: a matrix storing the time from one vertex to another by subway

    Subway_Cost_Table: a matrix storing the cost from one vertex to another by subway

    Taxi_Time_Table: a matrix storing the time from one vertex to another by taxi

    Taxi_Cost_Table: a matrix storing the cost from one vertex to another by taxi

"""
import TravelPlanner


if __name__ == "__main__":
    # Create a travel planner instance
    planner = TravelPlanner(attractions, hotels, subwayTimeTable, subwayCostTable, taxiTimeTable, taxiCostTable)

    # Optimize the travel plan
    bestSolution = planner.optimize()

    # Print the best solution found
    print(bestSolution)
