class Plan(object):
    def __init__(self):
        self.Day = 0
        self.Morning = {"text": "", "link": ""}
        self.Lunch_Recommendation = {"text": "", "link": ""}
        self.Afternoon = {"text": "", "link": ""}
        self.Dinner_Recommendation = {"text": "", "link": ""}
        self.Evening = {"text": "", "link": ""}
        self.Bedtime = {"text": "", "link": ""}

    def toDict(self):
        """
        :return: The dictionary of Plan
        """
        todict = dict()
        todict['Day'] = self.Day
        todict['Morning'] = self.Morning
        todict['Lunch_Recommendation'] = self.Lunch_Recommendation
        todict['Afternoon'] = self.Afternoon
        todict['Dinner_Recommendation'] = self.Dinner_Recommendation
        todict['Evening'] = self.Evening
        todict['Bedtime'] = self.Bedtime
        return todict
