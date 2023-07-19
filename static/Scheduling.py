"""
This Scheduling python file is aimed to implement the core functionality of Roam Assistant, which is generation of travel plan.
The process of generation of travel plan can be divided into these following parts:
    1. Retrieve data(e.g., attraction information) from database according to the user's input
    2. Use the related data to generate travel plan.
Aside from the core functionality, we need to also consider following aspects of our web-app:
    1. Network Communication:
        (1) How to access the database
        (2) How to communicate with Front-end RoamAssistantServer
        (3) How to use other APIs to get some information
    2. Further Adjustment:
        (1) How to handle the command of users to further adjustment
        (2) Whether to use the ChatGPT for help?
        (3) How to pre-train ChatGPT to satisfy our requirement
"""
from Entity.Attraction import Attraction
from Entity.TravelPlan import TravelPlanner
import copy
from EA.Main import EA_planning
from EA.Entity import Hotel
from EA.Entity import Attraction as EAttraction
attraction_list = []
import pymysql

conn = pymysql.connect(host='127.0.0.1'  # 连接名称，默认127.0.0.1
                       , user='root'  # 用户名
                       , passwd='Lipeiru129688'  # 密码
                       , port=3306  # 端口，默认为3306
                       , db='RoamAssistant'  # 数据库名称
                       , charset='utf8'  # 字符编码
                       )


def retrieve_data(destination: str):
    """
    Function [retrieve_data]:
        * Description: retrieve data from database according to the destination and store related information into attraction_list.
    :param destination:
    :return: None
    """
    cur = conn.cursor()  # 生成游标对象
    sql_search_city_id = "SELECT city_id FROM City WHERE city_name = '%s' " % destination
    cur.execute(sql_search_city_id)
    data = cur.fetchall()
    city_id = data[0]

    sql_search_attraction = "SELECT * FROM Attraction WHERE city_id = %d ORDER BY score DESC;" % (city_id)
    cur.execute(sql_search_attraction)
    data = cur.fetchall()
    for d in data:
        attraction_list.append(Attraction(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))

    cur.close()
    conn.close()
    return


def select_attraction_by_name(name: str):
    cur = conn.cursor()
    sql = "SELECT * FROM Attraction WHERE attraction_name = '%s';" % name
    # print(sql)
    cur.execute(sql)
    data = cur.fetchall()
    d = data[0]
    attraction = Attraction(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])
    cur.close()
    conn.close()
    return attraction


def select_country_by_city(city: str):
    cur = conn.cursor()
    sql = "select country_name from Country where country_id = (select country_id from City where city_name = '%s);" % city
    # print(sql)
    cur.execute(sql)
    data = cur.fetchall()
    d = data[0]
    return d[0]


def scheduling(departure: str, destination: str, days: int, first_dat: str):
    """
    function [scheduling]
        * description: make a travel scheduling according to the departure, destination and days
        * departure: where the tourist leave
        * destination: where the tourist want to visit
        * days: how long does the tourist want to stay in th destination

    The scheduling is divided into 3 parts
        1. Transportation
        2. Travel Plan
        3. Additional Information
    """
    travel_planner = TravelPlanner()
    # retrieve_data(destination)

    # Part 1: Transportation

    # Part 2: Travel Plan
    attractions_beijing = [
        EAttraction(index=1, referTime=3, timeWindow=(9, 17), referCost=30, name="故宫博物院"),
        EAttraction(index=2, referTime=5, timeWindow=(10, 16), referCost=100, name="八达岭长城"),
        EAttraction(index=3, referTime=12, timeWindow=(11, 18), referCost=100, name="端门"),
        EAttraction(index=4, referTime=2, timeWindow=(13, 19), referCost=0, name="颐和园"),
        EAttraction(index=5, referTime=3, timeWindow=(9, 17), referCost=0, name="恭王府"),
        EAttraction(index=6, referTime=3, timeWindow=(11, 17), referCost=15, name="天坛"),
        EAttraction(index=7, referTime=2, timeWindow=(12, 18), referCost=30, name="中国科学技术馆"),
        EAttraction(index=8, referTime=2, timeWindow=(17, 22), referCost=0, name="清华大学"),
        EAttraction(index=9, referTime=3, timeWindow=(9, 17), referCost=0, name="慕田峪长城"),
        EAttraction(index=10, referTime=2, timeWindow=(10, 16), referCost=0, name="北京动物园"),
        EAttraction(index=11, referTime=4, timeWindow=(11, 17), referCost=0, name="北京海洋馆"),
        EAttraction(index=12, referTime=5, timeWindow=(13, 19), referCost=0, name="北京欢乐谷"),
        EAttraction(index=13, referTime=3, timeWindow=(9, 17), referCost=0, name="南锣鼓巷")
    ]
    hotel_list = [
        Hotel(1, "北京乐多港万豪酒店", 204),
        Hotel(2, "北京兴基铂尔曼饭店", 241),
        Hotel(3, "北京亦庄智选假日酒店", 149),
        Hotel(4, "北京首都机场东海康得思酒店 - 朗廷酒店集团全新品牌", 170),
        Hotel(5, "北京古北口长城团园客栈", 91),
        Hotel(6, "北京临空皇冠假日酒店", 283)
    ]

    bestSolution = EA_planning(attractions_beijing, hotel_list=hotel_list)
    days = bestSolution.days
    hotel_index = bestSolution.hotel_index
    order = bestSolution.order

    for day in range(days):
        today_order = order[day]
        today_plan = {"Day": day + 1, "Attraction_List": [], "Accommodation": {"name": hotel_list[hotel_index].name, "text": "", "imgsrc": "", "details_url": ""}}
        for i in range(len(today_order)):
            attraction_index = today_order[i]
            attraction_name = attractions_beijing[attraction_index].name
            attraction = select_attraction_by_name(attraction_name)
            info_structure = {"order": i, "text": attraction.intro, "imgsrc": attraction.imgsrc, "details_url": attraction.details_url}
            today_plan["Attraction_List"].append(info_structure)
        travel_planner.travel_plans.append(today_plan)

    # Part 3: Additional Information
    country = select_country_by_city(destination)
    if country == "China":
        travel_planner.additional_information["Emergency_Number"] = "119"
        travel_planner.additional_information["Policy_Number"] = "110"
    else:
        travel_planner.additional_information["Emergency_Number"] = "995"
        travel_planner.additional_information["Policy_Number"] = "999"
    return travel_planner
