#-*- coding: utf_8 -*-

# *** Biblioteka funkcji implementujących algorytm knn ***
import math
import sys
sys.path.append('../common')
import sort  # noqa
import common  # noqa


def euclidean_metric_2d((x1, y1), (x2, y2)):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def manhattan_metric_2d((x1, y1), (x2, y2)):
    return abs(x1 - x2) + abs(y1 - y2)

# Resetuje liczniki sąsiadów i grup klas dla wybranego punktu

def info_reset(info):
    info['nbhd_count'] = 0
    info['class_count'] = {}
    


# Znajduje klasę sąsiada o współrzędnych (x, y)
# Jeśli klasa ta jest znana, sąsiad jest uwzględniany

def info_add(info, data, x, y):
    group = data.get((x, y), None)
    common.dic_inc(info['class_count'], group)
    info['nbhd_count'] += int(group is not None)


# Stosuje algorytm knn do danych dwuwymiarowych, uwzglęniając k najbliższych
# sąsiadów według metruki Manhattan.
# Współrzędne pełnią w słowniku rolę kluczy, wartiściami są klasy.
# Współrzędne (x, y) mieszczą się w zakresie [x_from,x_to] ... [y_from,y_to].


def knn_to_2d_data(data, x_from, x_to, y_from, y_to, k):
    new_data = {}
    info = {}
    # Przejdź przez wszystkie możliwe współrzędne
    for y in range(y_from, y_to + 1):
        for x in range(x_from, x_to + 1):
            info_reset(info)
                        
            # Uwzględnij liczbę sąsiadów dla każdej grupy klas i dla każdej
            # odległości począwszy od 0 aż do znalezienia co najmniej 
            # k sąsiadów o znanej klasie
            
            for dist in range(0, x_to - x_from + y_to - y_from):
                
                # Uwzględnij sąsiadów oddalonych o "dist" od badanego
                # punktu (x, y)
                if dist == 0:
                    info_add(info, data, x, y)
                else:
                    for i in range(0, dist + 1):
                        info_add(info, data, x - i, y + dist - i)
                        info_add(info, data, x + dist - i, y - i)
                    for i in range(1, dist):
                        info_add(info, data, x + i, y + dist - i)
                        info_add(info, data, x - dist + i, y - i)
                        
                
                # W tym miejscu możemy mieć więcej niż k najbliższych sąsiadów,
                # jeśli wiele znich mataką samą odległość od badanego punktu (x, y)
                # Gdy mamy ich co najmniej k, natychmiast przerywamy pętlę
                
                
                if info['nbhd_count'] >= k:
                    break
            class_max_count = None
            
            # Wybierz klasę o  największym liczniku sąsiadów 
            # spośród k najbliższych sąsiadów
            
            for group, count in info['class_count'].items():
                if group is not None and (class_max_count is None or
                   count > info['class_count'][class_max_count]):
                    class_max_count = group
            new_data[x, y] = class_max_count
    return new_data


# Bufor odległości, przechowujący obliczone odegłości w kolejności posortowanej


class DistBuffer:

    # metryka oblicza odległość między dwoma danymi punktami
    def __init__(self, metric):
        self.metric = metric
        self.dist_list = [(0, 0, 0)]
        self.pos = 0
        self.max_covered_dist = 0

    def reset(self):
        self.pos = 0

    def next(self):
        if self.pos < len(self.dist_list):
            (x, y, dist) = self.dist_list[self.pos]
            if dist <= self.max_covered_dist:
                self.pos += 1
                return (x, y)
        self.__loadNext()
        return self.next()

    
    # Ładuje więcej elementów do bufora, by więcej ich było dostepnych
    # dla metody next()
    def __loadNext(self):
        self.max_covered_dist += 1
        for x in range(-self.max_covered_dist, self.max_covered_dist + 1):
            self.__append(x, -self.max_covered_dist)
            self.__append(x, self.max_covered_dist)
        for y in range(-self.max_covered_dist + 1, self.max_covered_dist):
            self.__append(-self.max_covered_dist, y)
            self.__append(self.max_covered_dist, y)
        self.__sortList()

    def __append(self, x, y):
        self.dist_list.append((x, y, self.metric((0, 0), (x, y))))
        
        
# Assuming that the sorting algorithm does not change the order of the
# initial already sorted elements. This is so that next() does not skip
# some elements and returns a different element instead.
    def __sortList(self):
        self.dist_list.sort(key=proj_to_3rd)

    def printList(self):
        print self.dist_list


def proj_to_3rd((x, y, d)):
    return d


def less_than_on_3rd((x1, y1, d1), (x2, y2, d2)):
    return d1 < d2

# lookup_limit specifies at how many neighbors at most the algorithm
# should look at. In case it fails to find a class within that number
# of neighbors, the classification defaults to the value default.


def knn_to_2d_data_with_metric(data, x_from, x_to, y_from, y_to, k,
                               metric, lookup_limit, default):
    new_data = {}
    info = {}
    db = DistBuffer(metric)
    # Go through every point in an integer coordinate system.
    for y in range(y_from, y_to + 1):
        for x in range(x_from, x_to + 1):
            info_reset(info)
            db.reset()
            # Count the number of neighbors for each class group for
            # every distance dist starting at 0 until at least k
            # neighbors with known classes are found.
            lookup_count = 0
            while info['nbhd_count'] < k and lookup_count < lookup_limit:
                (x0, y0) = db.next()
                xn = x + x0
                yn = y + y0
                if x_from <= xn and xn <= x_to and y_from <= yn and yn <= y_to:
                    info_add(info, data, xn, yn)
                lookup_count += 1

            # Choose the class with the highest count of the neighbors
            # from among the k-closest neighbors.
            result = common.dic_key_max_count(info['class_count'])
            if result is None:
                new_data[x, y] = default
            else:
                new_data[x, y] = result
    return new_data
