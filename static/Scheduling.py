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

conn = pymysql.connect(host='roamassistantdatabase.cas2ra1clovs.us-east-1.rds.amazonaws.com'  # 连接名称，默认127.0.0.1
                       , user='admin'  # 用户名
                       , passwd='guidegenius'  # 密码
                       , port=3306  # 端口，默认为3306
                       , db='roamassistant'  # 数据库名称
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
    sql = "SELECT * FROM Attraction WHERE attraction_name = '%s'" % name
    print(sql)
    cur.execute(sql)
    data = cur.fetchall()
    d = data[0]
    attraction = Attraction(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])
    cur.close()
    return attraction


def select_country_by_city(city: str):
    cur = conn.cursor()
    sql = "select country_name from Country where country_id = (select country_id from City where city_name = '%s');" % city
    print(sql)
    cur.execute(sql)
    data = cur.fetchall()
    d = data[0]
    cur.close()
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
        EAttraction(index=1, referTime=3, timeWindow=(9, 17), referCost=30, name="故宫博物院",
                    information="The Forbidden City, also known as the Palace Museum, is an ancient imperial palace in Beijing. It served as the home to Chinese emperors for nearly 500 years and now houses a vast collection of historical artifacts and cultural treasures."),
        EAttraction(index=2, referTime=5, timeWindow=(10, 16), referCost=100, name="八达岭长城",
                    information="The Great Wall of China at Badaling, known as the Badaling Great Wall, is one of the most well-preserved and famous sections of the Great Wall. It offers breathtaking views and is a popular destination for tourists from around the world."),
        EAttraction(index=3, referTime=12, timeWindow=(11, 18), referCost=100, name="端门",
                    information="The National Museum of China is the largest comprehensive history and art museum in the country. It exhibits a rich collection of cultural relics and artworks that showcase China's long and diverse history."),
        EAttraction(index=4, referTime=2, timeWindow=(13, 19), referCost=0, name="颐和园",
                    information="The Summer Palace, or Yiheyuan, is a stunning imperial garden and palace in Beijing. It features beautiful pavilions, bridges, and a large lake, creating a picturesque and serene atmosphere."),
        EAttraction(index=5, referTime=3, timeWindow=(9, 17), referCost=0, name="恭王府",
                    information="Prince Gong's Mansion, or Gong Wang Fu, is an elegant and well-preserved residence of a Qing dynasty prince. Its traditional Chinese architecture and lush gardens provide a glimpse into China's royal past."),
        EAttraction(index=6, referTime=3, timeWindow=(11, 17), referCost=15, name="天坛",
                    information="The Temple of Heaven, or Tiantan, is an ancient religious complex where Chinese emperors performed sacrificial rituals. Its stunning architecture and serene surroundings make it a popular tourist attraction."),
        EAttraction(index=7, referTime=2, timeWindow=(12, 18), referCost=30, name="中国科学技术馆",
                    information="The China Science and Technology Museum is an interactive and educational space that showcases China's scientific achievements and technological advancements. It offers engaging exhibits and hands-on activities for visitors of all ages."),
        EAttraction(index=8, referTime=2, timeWindow=(17, 22), referCost=0, name="清华大学",
                    information="Tsinghua University is a prestigious academic institution located in Beijing, China. Renowned for its excellence in education and research, Tsinghua offers a wide range of disciplines and attracts top students and scholars from around the world. Its beautiful campus, rich history, and cutting-edge facilities make it a leading global university."),
        EAttraction(index=9, referTime=3, timeWindow=(9, 17), referCost=0, name="慕田峪长城",
                    information="Mutianyu Great Wall is another well-preserved section of the Great Wall known for its picturesque landscapes and ancient watchtowers. It's a less crowded option for those seeking a peaceful Great Wall experience."),
        EAttraction(index=10, referTime=2, timeWindow=(10, 16), referCost=0, name="北京动物园",
                    information="Beijing Zoo houses a wide variety of animals from all over the world, including pandas, elephants, and lions. It's a great place for families and animal enthusiasts to learn about wildlife conservation."),
        EAttraction(index=11, referTime=4, timeWindow=(11, 17), referCost=0, name="北京海洋馆",
                    information="Beijing Aquarium is a fascinating underwater world featuring various marine species. With impressive displays and interactive exhibits, it offers a delightful experience for visitors of all ages."),
        EAttraction(index=12, referTime=5, timeWindow=(13, 19), referCost=0, name="北京欢乐谷",
                    information="Happy Valley Beijing is a large amusement park filled with thrilling rides and entertainment options. It's a fantastic place for families and thrill-seekers to enjoy a day of fun and excitement."),
        EAttraction(index=13, referTime=3, timeWindow=(9, 17), referCost=0, name="南锣鼓巷",
                    information="Nanluoguxiang, or South Luogu Alley, is a charming traditional hutong street with an array of shops, cafes, and art galleries. It's a perfect place to experience Beijing's historical charm and shop for unique souvenirs.")
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
        today_plan = {"Day": day + 1, "Attraction_List": []}
        for i in range(len(today_order)):
            attraction_index = today_order[i]
            attraction_name = attractions_beijing[attraction_index].name
            attraction = select_attraction_by_name(attraction_name)
            info_structure = {"order": i,
                              # "text": attraction.intro,
                              "imgsrc": attraction.imgsrc,
                              "details_url": attraction.details_url,
                              "information": attractions_beijing[attraction_index].information}
            today_plan["Attraction_List"].append(info_structure)
        travel_planner.travel_plans.append(today_plan)

    # Part 3: Additional Information
    country = select_country_by_city(destination)
    travel_planner.accommodation["name"] = hotel_list[hotel_index].name
    if country == "China":
        travel_planner.additional_information["Emergency_Number"] = "119"
        travel_planner.additional_information["Policy_Number"] = "110"
    else:
        travel_planner.additional_information["Emergency_Number"] = "995"
        travel_planner.additional_information["Policy_Number"] = "999"

    if destination == "Beijing" or "北京":
        travel_planner.city_introduction = "Beijing, the vibrant capital of China, blends ancient history with modernity. The city is a treasure trove of cultural wonders, featuring iconic landmarks like the Great Wall, Forbidden City, and Temple of Heaven."
    if destination == "Singapore"  or "新加坡":
        travel_planner.city_introduction = "Singapore, a dynamic island city-state, captivates visitors with its blend of futuristic architecture, lush gardens, and diverse cultural influences. "
    return travel_planner
