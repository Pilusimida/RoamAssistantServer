class Attraction(object):
    def __init__(self, id, name, city_id, intro, score, position, imgsrc, url):
        self.attraction_id = id
        self.attraction_name = name
        self.city_id = city_id
        self.intro = intro
        self.score = score
        self.position = position
        self.imgsrc = imgsrc
        self.details_url = url
