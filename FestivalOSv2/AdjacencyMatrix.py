#!/usr/bin/env python3
# https://chatgpt.com/share/687ffe2c-b9c8-800c-8569-26c203e5ace2
from POI import POI
from MapManager import MapManager

class AdjacencyMatrix:

    DEBUG_STATEMENTS_ON = False

    def __init__(self, pointsOfInterest: list, navPoints: list):
        """
        Initialize the Adjacency Matrix setting first row and first column label as pointsOfInterest[] + navPoints[]

        Args:
            pointsOfInterest (list): List of points of interest.
            navPoints (list): List of navigation points.
        """
        self.POI_S = pointsOfInterest
        self.NAV_POINTS = navPoints
        self.num_vertices = len(pointsOfInterest) + len(navPoints)

        self.matrix = [[0 for _ in range(self.num_vertices)] for _ in range(self.num_vertices)]

        self.paths = [[[0] for _ in range(self.num_vertices)] for _ in range(self.num_vertices)]

        if AdjacencyMatrix.DEBUG_STATEMENTS_ON: print(f"Adjacency Matrix initialized with {self.num_vertices} vertices")


    def add_edge(self, startPoint: POI, endPoint: POI, length: int, path: list[int]):
        #print(f"Starting Point ID: {startPoint.id} & End Point ID: {endPoint.id}")
        self.matrix[startPoint.id][endPoint.id] = length
        self.matrix[endPoint.id][startPoint.id] = length
        self.paths[startPoint.id][endPoint.id] = path
        self.paths[endPoint.id][startPoint.id] = path[::-1] #Same as .reverse()

        if AdjacencyMatrix.DEBUG_STATEMENTS_ON: print(f"Adjacency Matrix updated to {self.matrix}")

    def define_adjacency_matrix(self):
        self.add_edge(self.POI_S[0], self.POI_S[1], 2, [self.POI_S[0].id, self.NAV_POINTS[1].id, self.POI_S[1].id])
        self.add_edge(self.POI_S[0], self.POI_S[2], 3, [self.POI_S[0].id, self.NAV_POINTS[1].id, self.NAV_POINTS[1].id, self.POI_S[2].id])
        self.add_edge(self.POI_S[1], self.POI_S[2], 2, [self.POI_S[1].id, self.NAV_POINTS[2].id, self.POI_S[2].id])


    def get_location(self, id: int):
        for point in self.POI_S:
            if point.id == id:
                return point.location
        for point in self.NAV_POINTS:
            if point.id == id:
                return point.location

        return None

    def find_path(self, startPoint: int, endPoint: int) -> list:
        if AdjacencyMatrix.DEBUG_STATEMENTS_ON:
            print(f"Looking for paths[{startPoint}][{endPoint}]")
            for i in range(self.num_vertices):
                print(f"Adjacency Paths Row # {i}: {self.paths[i]}")

        return self.paths[startPoint][endPoint]

    def find_length(self, u, v):
        return self.matrix[u][v]

    def new_map_center(self, startPoint: POI, endPoint: POI):
        newLat = (startPoint.location[0] + endPoint.location[0]) * 0.5
        newLong = (startPoint.location[1] + endPoint.location[1]) * 0.5

        return [newLat, newLong]

if __name__ == "__main__":
    """ https://www.mermaidchart.com/play#pako:eNqrVkrOT0lVslJKy8kvT85ILCpR8AmKyVMAgoD8zLwSQwUbXV07Bb_EMmQumG1MUBmMa4SkywhJlxGqMmNkw5VqAUQsLjM
    flowchart LR
        X Booth <--> NavPoint0 <--> Y Booth
        X Booth <--> NavPoint0 <--> NavPoint1 <--> Z Booth
        Y Booth <--> NavPoint2 <--> Z Booth

    """

    # Define Points of Interests (POIs) and Navigation Points (NavPoints)
    POIs = [POI("X Booth",    [45.5239, -122.6755], MapManager.GREEN, MapManager.BOOTH, "TODO"),
            POI("Y Booth",    [45.5242, -122.6759], MapManager.GREEN, MapManager.BOOTH, "TODO"),
            POI("Z Booth",    [45.5239, -122.6765], MapManager.GREEN, MapManager.BOOTH, "TODO")]

    NavPoints = [POI("Map Center", [45.5236, -122.6750], MapManager.BLUE, MapManager.NAV, "https://maps.app.goo.gl/6KYesGps9J3xgzvp6"),
                 POI("TouchScreen 1", [45.5236, -122.6755], MapManager.RED, MapManager.INFO, "TODO"),
                 POI("Navigation Point 1", [45.5236, -122.6759], MapManager.BLACK, MapManager.NAV, "TODO")]

    adjMatrix = AdjacencyMatrix(POIs, NavPoints)
    print(f"Printing POI's index 0: {adjMatrix.POI_S[0]}")

    # Update POI IDs and add markers and poly path to map
    lastIdUsed = 0
    for i, poi in enumerate(POIs):
        poi.id = i
        lastIdUsed = i

    for i, navPoint in enumerate(NavPoints):
        navPoint.id = lastIdUsed + i


    # Add 3 edges for ["Point0", "Point1", "Point2", "NavPoint0", "NavPoint1", "NavPoint2"]
    adjMatrix.add_edge(adjMatrix.POI_S[0], adjMatrix.POI_S[1], 2, [adjMatrix.POI_S[0].id, adjMatrix.NAV_POINTS[2].id, adjMatrix.POI_S[1].id])
    adjMatrix.add_edge(adjMatrix.POI_S[0], adjMatrix.POI_S[2], 3, [adjMatrix.POI_S[0].id, adjMatrix.NAV_POINTS[2].id, adjMatrix.NAV_POINTS[1].id, adjMatrix.POI_S[2].id])
    adjMatrix.add_edge(adjMatrix.POI_S[1], adjMatrix.POI_S[2], 2, [adjMatrix.POI_S[1].id, adjMatrix.NAV_POINTS[2].id, adjMatrix.POI_S[2].id])

    distance = adjMatrix.find_length(0, 1)
    print(f"Distance between {adjMatrix.POI_S[0]} and {adjMatrix.POI_S[1]} is {distance}")

    foundPath = adjMatrix.find_path(adjMatrix.POI_S[0].id, adjMatrix.POI_S[1].id)
    print(f"Path from {adjMatrix.POI_S[0]} to {adjMatrix.POI_S[1]} is {foundPath}")

    gnssPath = []
    for searchiD in foundPath:
        gnssPath.append(adjMatrix.get_location(searchiD))
    print(gnssPath)
