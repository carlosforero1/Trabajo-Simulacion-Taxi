import pygame
import tkinter as tk

class Application(tk.Tk):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.title("Mapa de Carro")
        self.geometry("300x200")

        self.start_label = tk.Label(self, text="Inicio:")
        self.start_label.pack()
        self.start_entry = tk.Entry(self)
        self.start_entry.pack()

        self.end_label = tk.Label(self, text="Destino:")
        self.end_label.pack()
        self.end_entry = tk.Entry(self)
        self.end_entry.pack()

        self.submit_button = tk.Button(self, text="Encontrar Ruta", command=self.find_route)
        self.submit_button.pack()

    def find_route(self):
        start = self.start_entry.get()
        end = self.end_entry.get()
        path = self.graph.shortest_path(start, end)
        print(f"Ruta más corta: {path}")
        VisualizeMap(self.graph, path)


class VisualizeMap:
    def __init__(self, graph, path):
        self.graph = graph
        self.path = path
        self.node_positions = {
            'A': (50, 50), 'B': (150, 50), 'C': (250, 50),
            'D': (50, 150), 'E': (250, 150), 'F': (150, 150),
            'G': (250, 250), 'H': (50, 250)
        }
        self.run()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((300, 300))
        pygame.display.set_caption("Mapa de Carro")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))

            # Draw edges
            for vertex, edges in self.graph.vertices.items():
                for neighbor, weight in edges.items():
                    start_pos = self.node_positions[vertex]
                    end_pos = self.node_positions[neighbor]
                    pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)

            # Draw nodes
            for vertex, pos in self.node_positions.items():
                color = (0, 255, 0) if vertex in self.path else (0, 0, 255)
                pygame.draw.circle(screen, color, pos, 10)
                label = pygame.font.SysFont(None, 24).render(vertex, True, (0, 0, 0))
                screen.blit(label, (pos[0] - 10, pos[1] - 10))

            # Draw path
            if self.path:
                for i in range(len(self.path) - 1):
                    start_pos = self.node_positions[self.path[i]]
                    end_pos = self.node_positions[self.path[i + 1]]
                    pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 2)

            pygame.display.flip()

        pygame.quit()
