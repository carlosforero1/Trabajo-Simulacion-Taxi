import heapq
import sys

class Graph:
    def __init__(self):
        self.vertices = {}
        self.node_positions = {}  # Diccionario para almacenar las posiciones (x, y) de los nodos

    def add_vertex(self, name, edges, x=None, y=None):
        self.vertices[name] = edges
        if x is not None and y is not None:
            self.node_positions[name] = (x, y)

    def shortest_path(self, start, finish):
        distances = {}
        previous = {}
        nodes = []

        for vertex in self.vertices:
            if vertex == start:
                distances[vertex] = 0
                heapq.heappush(nodes, [0, vertex])
            else:
                distances[vertex] = sys.maxsize
                heapq.heappush(nodes, [sys.maxsize, vertex])
            previous[vertex] = None

        while nodes:
            smallest = heapq.heappop(nodes)[1]
            if smallest == finish:
                path = []
                while previous[smallest]:
                    path.append(smallest)
                    smallest = previous[smallest]
                path.append(start)
                path.reverse()
                return path
            if distances[smallest] == sys.maxsize:
                break

            for neighbor in self.vertices[smallest]:
                alt = distances[smallest] + self.vertices[smallest][neighbor]
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = smallest
                    for n in nodes:
                        if n[1] == neighbor:
                            n[0] = alt
                            break
                    heapq.heapify(nodes)
        return distances

    def __str__(self):
        return str(self.vertices)
