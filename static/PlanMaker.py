'''
Here is the code of Plan Maker, which send back a static travel plan based on our database.
'''
import json


class DailyRoutine:
    def __init__(self, index: int):
        self.index = index
        self.morning = ''
        self.lunch = ''
        self.afternoon = ''
        self.dinner = ''
        self.evening = ''

    def toJson(self):
        daily_routine = {'index': self.index, 'morning': self.morning, 'lunch': self.lunch, 'afternoon': self.afternoon,
                         'evening': self.evening}
        print("Daily Routine " + str(self.index) + ": to json format---------->")
        return json.dumps(daily_routine);


# this list will later be extracted from database
Attractions_in_Singapore = [
    "Marina Bay Sands",
    "Gardens by the Bay",
    "Universal Studios Singapore",
    "Sentosa Island",
    "Merlion Park",
    "Singapore Flyer",
    "Orchard Road",
    "Chinatown",
    "Little India",
    "Clarke Quay",
    "Raffles Hotel",
    "National Museum of Singapore",
    "Singapore Botanic Gardens",
    "Sri Mariamman Temple",
    "Jurong Bird Park",
    "Singapore Zoo",
    "ArtScience Museum",
    "Asian Civilisations Museum",
    "Fort Canning Park",
    "Haw Par Villa",
    "East Coast Park"
]
Days = 3
if __name__ == "__main__":
    Travel = {"days":[]}
    for i in range(Days):
        dr = DailyRoutine(i)
        dr.morning = Attractions_in_Singapore[3*i]
        dr.afternoon = Attractions_in_Singapore[3*i+1]
        dr.evening = Attractions_in_Singapore[3*i + 2]
        Travel['days'].append(dr.toJson())
        print("Daily Routine "+str(i)+" is generated successfully!")
    print(Travel)
