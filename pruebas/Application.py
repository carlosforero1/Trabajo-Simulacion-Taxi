import math

import pygame
import tkinter as tk
from tkinter import ttk

import self


class Application(tk.Tk):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.title("Mapa de Carro")
        self.geometry("600x500")

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

        self.tree = ttk.Treeview(self)

        self.tree['columns'] = ('Lugares')

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Lugares", anchor=tk.CENTER, width=120)

        self.tree.heading("#0", text="", anchor=tk.CENTER)
        self.tree.heading("Lugares", text="Lugares", anchor=tk.CENTER)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.map('Treeview', background=[('selected', 'blue')])

        self.tree.tag_configure('oddrow', background="lightblue")
        self.tree.tag_configure('evenrow', background="lightyellow")

        data = [
            ("Chipre"),
            ("Cable"),
            ("Sultana"),
            ("Lusitania"),
            ("Bosque"),
            ("Enea"),
            ("Terminal"),
            ("Villa"),
        ]

        for count, item in enumerate(data):
            if count % 2 == 0:
                self.tree.insert('', 'end', values=item, tags=('evenrow',))
            else:
                self.tree.insert('', 'end', values=item, tags=('oddrow',))

        self.tree.pack(pady=20)

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
        self.node_positions = self.graph.node_positions
        self.current_segment = 0  # Índice del segmento actual en la ruta
        self.segment_progress = 0.0  # Progreso dentro del segmento actual (0.0 a 1.0)
        self.taxi_position = None
        self.taxi_speed = 2  # Velocidad de movimiento del taxi
        self.run()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Mapa de Carro")

        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))

            # Dibujar aristas
            for vertex, edges in self.graph.vertices.items():
                for neighbor, weight in edges.items():
                    start_pos = self.node_positions[vertex]
                    end_pos = self.node_positions[neighbor]
                    pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)

            # Dibujar nodos
            for vertex, pos in self.node_positions.items():
                pygame.draw.circle(screen, (0, 255, 0), pos, 10)
                label = pygame.font.SysFont(None, 24).render(vertex, True, (0, 0, 0))
                screen.blit(label, (pos[0] - 10, pos[1] - 10))

            # Dibujar ruta más corta
            if self.path:
                for i in range(len(self.path) - 1):
                    start_pos = self.node_positions[self.path[i]]
                    end_pos = self.node_positions[self.path[i + 1]]
                    pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 2)

            # Mover el taxi a lo largo de la ruta
            if self.current_segment < len(self.path) - 1:
                start_pos = self.node_positions[self.path[self.current_segment]]
                end_pos = self.node_positions[self.path[self.current_segment + 1]]

                # Calcular el punto intermedio en el segmento actual
                segment_length = math.dist(start_pos, end_pos)
                if segment_length > 0:
                    dx = (end_pos[0] - start_pos[0]) / segment_length
                    dy = (end_pos[1] - start_pos[1]) / segment_length
                else:
                    dx, dy = 0, 0

                self.segment_progress += self.taxi_speed / segment_length
                if self.segment_progress >= 1.0:
                    # Pasar al siguiente segmento
                    self.current_segment += 1
                    self.segment_progress = 0.0

                    # Ajustar posición inicial del próximo segmento
                    if self.current_segment < len(self.path) - 1:
                        start_pos = self.node_positions[self.path[self.current_segment]]
                        end_pos = self.node_positions[self.path[self.current_segment + 1]]
                        segment_length = math.dist(start_pos, end_pos)
                        self.segment_progress = self.taxi_speed / segment_length

                if self.current_segment < len(self.path) - 1:
                    # Calcular posición actual del taxi
                    current_pos = (start_pos[0] + dx * segment_length * self.segment_progress,
                                   start_pos[1] + dy * segment_length * self.segment_progress)

                    self.taxi_position = current_pos

            # Dibujar el taxi
            if self.taxi_position:
                pygame.draw.circle(screen, (255, 0, 0), (int(self.taxi_position[0]), int(self.taxi_position[1])), 8)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
    def is_within_screen(self, position, screen):
        # Verificar si la posición está dentro de los límites de la pantalla
        return 0 <= position[0] <= screen.get_width() and 0 <= position[1] <= screen.get_height()

    def adjust_position_within_screen(self, position, screen):
        # Ajustar la posición para que esté dentro de los límites de la pantalla
        x = min(max(position[0], 0), screen.get_width())
        y = min(max(position[1], 0), screen.get_height())
        return (x, y)

