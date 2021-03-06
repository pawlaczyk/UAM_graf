#coding=utf-8

"""
Graf w przestrzeni
"""

from abc import ABCMeta, abstractmethod
import numpy as np

from api.point import PointBase, Point1D, Point2D
from api.sphere import Sphere2D, SphereBase


class GraphBase(metaclass=ABCMeta):
    """
    Wierzchołki w przestrzeni
    Kompozycja
    """
    _dimension = None  # atrybut klasy

    @abstractmethod
    def __init__(self, spaceObj, point_list, weight):
        # type: (Union[SphereBase, Any], Union[int, float], List[PointBase]) -> None

        self.spaceObj = spaceObj  # przestrzeń
        self.point_list = point_list
        self.weight = weight


    @abstractmethod
    def checkEdgeBetweenPointsExists(self, pointA, pointB):
        # type: (Point, Point) -> bool
        """
        Sprawdzanie czy pomiędzy punktami istnieje krawędź
        """
        pass

    @classmethod
    def fromEmptyPointsAndEmptySphere(cls, sphereRadius, totalPoints): #Konstruktor alternatywny
        """Sam generuje liste punktów i tworzy przestrzeń
        """
        pass

    @abstractmethod
    def createGraphMatrix(self, weight):
        """
        Zwraca mapę sąsiedztwa między punktami
        :param weight:
        """
        pass


class Graph1D(GraphBase):

    def __init__(self, spaceObj, point_list, weight):
        # type: (Sphere, Union[int, float], List[Point1D]) -> None
        super(Graph1D, self).__init__(spaceObj, point_list, weight)

    def checkEdgeBetweenPointsExists(self, pointA, pointB):
        # type: (Point, Point) -> bool
        pass


    def createGraphMatrix(self, weight):
        pass

    @classmethod
    def fromEmptyPointsAndEmptySphere(cls, sphereRadius, totalPoints): #Konstruktor alternatywny
        """Sam generuje liste punktów i tworzy przestrzeń
        """
        pass


class Graph2D(Graph1D):

    def __init__(self, spaceObj, point_list, weight):
        # type: (Sphere2D, Union[int, float], List[Point]) -> None
        # kompozycja
        self.weight = weight
        super(Graph2D, self).__init__(spaceObj, point_list, weight)

    def checkEdgeBetweenPointsExists(self, pointA, pointB):
        # type: (Point2D, Point2D) -> bool
        """
        Krawędź miedzy wierzchołkami jest wtedy, gdy odległośc między nimi <= (2*waga)**2
        """
        if (abs(pointA.x - pointB.x)**2 + abs(pointA.y - pointB.y)**2) <= 4*(self.weight**2):
            return True
        return False


    @classmethod
    def fromEmptyPointsAndEmptySphere(cls, sphereRadius, totalPoints, weight): #Konstruktor alternatywny
        # type:(Union[int, float], int, Union[int, float] -> Graph2D
        """Sam generuje liste punktów i tworzy przestrzeń a nastepnie zwraca obiekt grafu
        """
        point_list = []
        for i in range(totalPoints):
            point_list.append(Point2D.fromRandom(sphereRadius))

        spaceObj = Sphere2D(sphereRadius)
        return cls(spaceObj, point_list, weight)


    def createGraphMatrix(self):
        matrixSize = len(self.point_list)
        graphMatrix = np.zeros((matrixSize, matrixSize))

        for index1, point1 in enumerate(self.point_list):
            for index2, point2 in enumerate(self.point_list):
                if self.checkEdgeBetweenPointsExists(point1, point2) and point1 is not point2:
                    # porówannie referencji obiektów - teoretycznie można wylosowac dwa punkty o tych samymch
                    # wartościach i je trzeba rozpatrywać jako dwa osobne punkty
                    graphMatrix[index1][index2] = int(1)

        return graphMatrix


    def __str__(self):
        return "Graf na płaszczyźnie 2D"
