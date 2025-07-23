#!/usr/bin/env python3
import MapManager

class POI:

    def __init__(self, name: str, location: list, color: str, iconImage: str):
        """ Initialize a POI object with a name, location, color, and icon image.
            https://ionic.io/ionicons
        """
        self.id = -1
        self.name = name
        self.location = location
        self.lat = location[0]
        self.long = location[1]
        self.color = color
        self.iconImage = iconImage

    def __str__(self):
        return f"{self.name}"

    def enumerate_poi(self, POIs: list, NavPoints: list):
        lastIdUsed = 0
        for i, poi in enumerate(POIs):
            poi.id = i
            lastIdUsed = i

        for i, navPoint in enumerate(NavPoints):
            navPoint.id = lastIdUsed + i

    def find_point_of_interest(self, name: str, search: list):
        for poi in search:
            if poi.name == name:
                return poi.id

        return None
