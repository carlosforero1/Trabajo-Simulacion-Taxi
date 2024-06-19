from pruebas.Application import Application
from pruebas.Graph import Graph

if __name__ == '__main__':
    g = Graph()
    g.add_vertex('Chipre', {'Cable': 7, 'Sultana': 8}, 50, 50)
    g.add_vertex('Cable', {'Chipre': 7, 'Enea': 2}, 150, 50)
    g.add_vertex('Sultana', {'Chipre': 8, 'Enea': 6, 'Terminal': 4}, 250, 50)
    g.add_vertex('Lusitania', {'Enea': 8}, 50, 150)
    g.add_vertex('Bosque', {'Villa': 1}, 250, 150)
    g.add_vertex('Enea', {'Cable': 2, 'Sultana': 6, 'Lusitania': 8, 'Terminal': 9, 'Villa': 3}, 150, 150)
    g.add_vertex('Terminal', {'Sultana': 4, 'Enea': 9}, 250, 250)
    g.add_vertex('Villa', {'Bosque': 1, 'Enea': 3}, 50, 250)

    app = Application(g)
    app.mainloop()

