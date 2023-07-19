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
from EA.Entity import Attraction, Hotel, TravelPlanner
import random
import matplotlib.pyplot as plt
from EA.Reader import readCSV

# Define attractions
# attractions_sg = [
#     Attraction(index=0, referTime=3, timeWindow=(9, 17), referCost=30, name="Gardens by the Bay"),
#     Attraction(index=1, referTime=5, timeWindow=(10, 16), referCost=100, name="Singapore Zoo"),
#     Attraction(index=2, referTime=12, timeWindow=(11, 18), referCost=100, name="Sentosa Island"),
#     Attraction(index=3, referTime=2, timeWindow=(13, 19), referCost=0, name="Singapore Riverfront"),
#     Attraction(index=4, referTime=3, timeWindow=(9, 17), referCost=0, name="Botanic Gardens"),
#     Attraction(index=5, referTime=2, timeWindow=(17, 22), referCost=0, name="Clarke Quay"),
#     Attraction(index=6, referTime=3, timeWindow=(11, 17), referCost=15, name="National Museum of Singapore"),
#     Attraction(index=7, referTime=2, timeWindow=(12, 18), referCost=30, name="Marina Bay Sands"),
#     Attraction(index=8, referTime=2, timeWindow=(17, 22), referCost=0, name="Chinatown")
# ]
# attractions_beijing = [
#     Attraction(index=0, referTime=3, timeWindow=(9, 17), referCost=30, name="故宫博物院"),
#     Attraction(index=1, referTime=5, timeWindow=(10, 16), referCost=100, name="八达岭长城"),
#     Attraction(index=2, referTime=12, timeWindow=(11, 18), referCost=100, name="中国国家博物馆"),
#     Attraction(index=3, referTime=2, timeWindow=(13, 19), referCost=0, name="颐和园"),
#     Attraction(index=4, referTime=3, timeWindow=(9, 17), referCost=0, name="恭王府"),
#     # Attraction(index=5, referTime=2, timeWindow=(17, 22), referCost=0, name="中国人民革命军事博物馆"),
#     Attraction(index=6, referTime=3, timeWindow=(11, 17), referCost=15, name="天坛"),
#     Attraction(index=7, referTime=2, timeWindow=(12, 18), referCost=30, name="中国科学技术馆"),
#     Attraction(index=8, referTime=2, timeWindow=(17, 22), referCost=0, name="圆明园"),
#     Attraction(index=9, referTime=3, timeWindow=(9, 17), referCost=0, name="慕田峪长城"),
#     Attraction(index=10, referTime=2, timeWindow=(10, 16), referCost=0, name="北京动物园"),
#     Attraction(index=11, referTime=4, timeWindow=(11, 17), referCost=0, name="北京海洋馆"),
#     Attraction(index=12, referTime=5, timeWindow=(13, 19), referCost=0, name="北京欢乐谷"),
#     Attraction(index=13, referTime=3, timeWindow=(9, 17), referCost=0, name="南锣鼓巷")
# ]

# Define hotels
# hotels = [
#     Hotel(1, "北京乐多港万豪酒店", 204),
#     Hotel(2, "北京兴基铂尔曼饭店", 241),
#     Hotel(3, "北京亦庄智选假日酒店", 149),
#     Hotel(4, "北京首都机场东海康得思酒店 - 朗廷酒店集团全新品牌", 170),
#     Hotel(5, "北京古北口长城团园客栈", 91),
#     Hotel(6, "北京临空皇冠假日酒店", 283)
# ]


# Calculate the total number of vertices (attractions + hotels)
# num_vertices = len(attractions_beijing) + len(hotels)

# Define subway time and cost tables
subwayTimeTable_a = readCSV('bus-time.csv') / 3600
subwayCostTable_a = readCSV('bus-cost.csv')

# Define taxi time and cost tables
taxiTimeTable_a = readCSV('taxi-time.csv') / 3600
taxiCostTable_a = readCSV('taxi-cost.csv')

# Define subway time and cost tables
subwayTimeTable_h = readCSV('HotelToAttracByBus-time.csv') / 3600
subwayCostTable_h = readCSV('HotelToAttracByBus-cost.csv')

# Define taxi time and cost tables
taxiTimeTable_h = readCSV('HotelToAttracByTaxi-time.csv') / 3600
taxiCostTable_h = readCSV('HotelToAttracByTaxi-cost.csv')


def EA_planning(attraction_list: list, hotel_list: list):
    # Create a travel planner instance
    planner = TravelPlanner(attraction_list, hotel_list,
                            subwayTimeTable_a, subwayCostTable_a, taxiTimeTable_a, taxiCostTable_a,
                            subwayTimeTable_h, subwayCostTable_h, taxiTimeTable_h, taxiCostTable_h)
    # Optimize the travel plan
    [bestSolution, best_record, avg_record] = planner.optimize()

    # Print the best solution found
    print("Best Travel Plan")
    best_hotel = hotel_list[bestSolution.hotel_index]
    print(f"Hotel: {best_hotel.name}/${best_hotel.expenses} per night")
    print("Visit Order: ", end="")
    print(len(bestSolution.attraction_order))
    print(bestSolution.order)
    day = 0
    for index in bestSolution.order:
        if index < 0:
            print("")
            day += 1
            print(f"Day: {day}")
            print(hotel_list[-index-1].name, end="->")
        else:
            print(f"{attraction_list[index].name}", end="->")
    print(f"\nTotal: ")
    print(f"-->Days: {bestSolution.days}")
    print(f"-->Cost: {bestSolution.cost}")
    print(f"-->Time: {bestSolution.time}")
    bestSolution.order = split_array(bestSolution.order)
    print(bestSolution.order)

    # Visualize the process of EA
    # generation = range(len(best_record))

    # # Plot the best solution and average value over generations
    # plt.plot(generation, best_record, label='Best Solution')
    # plt.plot(generation, avg_record, label='Average Value')
    #
    # plt.xlabel('Generation')
    # plt.ylabel('Fitness Value')
    # plt.title('Optimization Process')
    # plt.legend()
    # plt.savefig("plot.png")
    # plt.show()
    return bestSolution


def split_array(arr):
    result = []
    sublist = []
    for num in arr:
        if num < 0:
            if sublist:
                result.append(sublist)
                sublist = []
        else:
            sublist.append(num)

    if sublist:
        result.append(sublist)

    return result

