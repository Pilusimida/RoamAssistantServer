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
from static.Attraction import Attraction
from static.TravelPlan import TravelPlanner
import copy

attraction_list = []
import pymysql

conn = pymysql.connect(host='roamassistantdatabase.cas2ra1clovs.us-east-1.rds.amazonaws.com'  # 连接名称，默认127.0.0.1
                       , user='admin'  # 用户名
                       , passwd='guidegenius'  # 密码
                       , port=3306  # 端口，默认为3306
                       , db='roamassistantdatabase'  # 数据库名称
                       , charset='utf8'  # 字符编码
                       )



def retrieve_data(destination:str):
    """
    Function [retrieve_data]:
        * Description: retrieve data from database according to the destination and store related information into attraction_list.
    :param destination:
    :return: None
    """
    cur = conn.cursor()  # 生成游标对象
    sql_search_city_id = "SELECT city_id FROM City WHERE city_name = '%s' " % (destination)
    cur.execute(sql_search_city_id)
    data = cur.fetchall()
    city_id = data[0]

    sql_search_attraction = "SELECT * FROM Attraction WHERE city_id = %d ORDER BY score DESC;" % (city_id)
    cur.execute(sql_search_attraction)
    data = cur.fetchall()
    for d in data:
        attraction_list.append(Attraction(d[0], d[1], d[2],d[3], d[4], d[5], d[6], d[7]))

    cur.close()
    # conn.close()
    return


def scheduling(departure:str, destination:str, days:int, first_dat:str):
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
    retrieve_data(destination)

    # Part 1: Transportation

    # Part 2: Travel Plan
    ptr = 0
    for day in range(days):
        demo_plan = copy.deepcopy(travel_planner.demo_plan)
        demo_plan['Day'] = day + 1
        demo_plan['Morning']['text'] = attraction_list[ptr].intro
        demo_plan['Morning']['link'] = attraction_list[ptr].imgsrc
        ptr = ptr + 1

        demo_plan['Afternoon']['text'] = attraction_list[ptr].intro
        demo_plan['Afternoon']['link'] = attraction_list[ptr].imgsrc
        ptr = ptr + 1

        demo_plan['Evening']['text'] = attraction_list[ptr].intro
        demo_plan['Evening']['link'] = attraction_list[ptr].imgsrc
        ptr = ptr + 1

        travel_planner.travel_plans.append(demo_plan)

    # Part 3: Additional Information

    return travel_planner
