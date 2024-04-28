# -*- coding: utf-8 -*-
"""B.2 ( Part B )

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1POa0xgYBG_H5Hw_HqrTRY7-nK6VXes70
"""

import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Intersection:
    def __init__(self, intersection_id):
        self.id = intersection_id
        self.adjacent = {}  # {neighbor_intersection_id: road_info}

    def add_neighbor(self, neighbor, road_info):
        self.adjacent[neighbor] = road_info


class RoadNetwork:
    def __init__(self):
        self.intersections = {}
        self.houses = {}

    def add_intersection(self, intersection_id):
        if intersection_id not in self.intersections:
            self.intersections[intersection_id] = Intersection(intersection_id)

    def add_road(self, start_intersection, end_intersection, road_id, road_name, length):
        if start_intersection not in self.intersections:
            self.add_intersection(start_intersection)
        if end_intersection not in self.intersections:
            self.add_intersection(end_intersection)

        self.intersections[start_intersection].add_neighbor(end_intersection, {'road_id': road_id, 'road_name': road_name, 'length': length})

    def add_house(self, house_id, intersection_id):
        self.houses[house_id] = intersection_id

    def dijkstra_shortest_path(self, start_intersection, end_intersection):
        distances = {intersection_id: float('inf') for intersection_id in self.intersections}
        distances[start_intersection] = 0
        heap = [(0, start_intersection)]

        while heap:
            current_distance, current_intersection = heapq.heappop(heap)

            if current_distance > distances[current_intersection]:
                continue

            if current_intersection == end_intersection:
                return distances[end_intersection]

            for neighbor_intersection, road_info in self.intersections[current_intersection].adjacent.items():
                distance = current_distance + road_info['length']
                if distance < distances[neighbor_intersection]:
                    distances[neighbor_intersection] = distance
                    heapq.heappush(heap, (distance, neighbor_intersection))

        return float('inf')

    def plot_graph(self):
        G = nx.DiGraph()

        for intersection_id, intersection in self.intersections.items():
            G.add_node(intersection_id)

            for neighbor_intersection, road_info in intersection.adjacent.items():
                G.add_edge(intersection_id, neighbor_intersection, length=road_info['length'])

        for house_id, intersection_id in self.houses.items():
            G.add_node(house_id)
            G.add_edge(intersection_id, house_id, length=1)  # Assuming distance from intersection to house is 1

        pos = nx.spring_layout(G, seed=42)  # Improved layout for better spacing

        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=10, font_weight="bold")
        nx.draw_networkx_edge_labels(G, pos, font_color='black', edge_labels=nx.get_edge_attributes(G, 'length'))
        plt.title("Road Network with Houses Graph")
        plt.show()


# Example Usage
city_road_network = RoadNetwork()
city_road_network.add_road(101, 102, 1, "Road 1", 5)
city_road_network.add_road(102, 103, 2, "Road 2", 4)
city_road_network.add_road(101, 103, 3, "Road 3", 8)
city_road_network.add_road(103, 104, 4, "Road 4", 6)
city_road_network.add_road(104, 105, 5, "Road 5", 7)
city_road_network.add_road(105, 106, 6, "Road 6", 3)
city_road_network.add_road(106, 107, 7, "Road 7", 5)
city_road_network.add_road(107, 108, 8, "Road 8", 4)
city_road_network.add_road(108, 109, 9, "Road 9", 6)
city_road_network.add_road(109, 110, 10, "Road 10", 8)

# Adding houses with IDs 1, 2, 3
city_road_network.add_house(1, 102)  # House 1 is closest to Intersection 102
city_road_network.add_house(2, 101)  # House 2 is closest to Intersection 101
city_road_network.add_house(3, 103)  # House 3 is closest to Intersection 103

city_road_network.plot_graph()

start_point = int(input("Enter the ID of the starting point (intersection or house): "))
end_point = int(input("Enter the ID of the ending point (intersection or house): "))

shortest_distance = city_road_network.dijkstra_shortest_path(start_point, end_point)

if shortest_distance == float('inf'):
    print("No path exists between the specified points.")
else:
    print(f"Shortest Distance from {start_point} to {end_point}: {shortest_distance}")