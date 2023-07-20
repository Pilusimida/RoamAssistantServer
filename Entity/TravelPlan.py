import json

'''
This is a python class "TravelPlanner" for transmission of data in Roam Assistant
consisting of "transportations", "travel_plans" and "additional_information", which are all in the format of dictionary.

'''


class TravelPlanner(object):
    def __init__(self):
        # self.transportations = {"Flight": {"text": "", "link": ""}, "Train": {"text": "", "link": ""}}
        self.travel_plans = []
        self.additional_information = {"Policy_Number": "", "Emergency_Number": ""}
        self.demo_plan = {
            "Day": 0,
            "Morning": {
                "text": "Start your day with a visit to the iconic Merlion Park, where you can see the famous Merlion statue, a mythical creature with the head of a lion and the body of a fish. Enjoy panoramic views of the city skyline and Marina Bay from this picturesque location.",
                "imgsrc": "",
                "details_url": ""
            },
            "Lunch_Recommendation": {
                "text": "You can have lunch in 'Jypsy at One Fullerton near Merlion Park",
                "imgsrc": "",
                "details_url": ""
            },
            "Afternoon": {
                "text": "Head to the Supertree Grove at Gardens by the Bay, a futuristic park with towering tree-like structures. Explore the various gardens and attractions, such as the Flower Dome and Cloud Forest, and admire the stunning views of the city from the OCBC Skyway.",
                "imgsrc": "",
                "details_url": ""
            },
            "Dinner_Recommendation": {
                "text": "You can have dinner at 'Marina Bay BBQ Steamboat Buffet inside Garden by the Bay",
                "imgsrc": "",
                "details_url": ""
            },
            "Evening": {
                "text": "Take a leisurely stroll along the Singapore River and enjoy the vibrant atmosphere of Clarke Quay. Indulge in a delicious dinner at one of the riverside restaurants and take a river cruise to see the cityscape illuminated at night.",
                "imgsrc": "",
                "details_url": ""
            },
            "Bedtime": {
                "text": "You can find amazing hotels here: ",
                "link": "https://www.kayak.sg/hotels/Singapore/2023-07-12/2023-07-16?sort=rank_a"
            }
        }

    def toJSON(self):
        travelPlanner = {"Travel_Plans": self.travel_plans,
                         "Additional_Information": self.additional_information}
        return json.dumps(travelPlanner)
