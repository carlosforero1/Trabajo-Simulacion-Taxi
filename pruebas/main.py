from pruebas.Application import Application
from pruebas.Graph import Graph

if __name__ == '__main__':
    g = Graph()
    g.add_vertex('Chipre', {'Cable': 7, 'Sultana': 8})
    g.add_vertex('Cable', {'Chipre': 7, 'Enea': 2})
    g.add_vertex('Sultana', {'Chipre': 8, 'Enea': 6, 'Terminal': 4})
    g.add_vertex('Lusitania', {'Enea': 8})
    g.add_vertex('Bosque', {'Villa': 1})
    g.add_vertex('Enea', {'Cable': 2, 'Sultana': 6, 'Lusitania': 8, 'Terminal': 9, 'Villa': 3})
    g.add_vertex('Terminal', {'Sultana': 4, 'Enea': 9})
    g.add_vertex('Villa', {'Bosque': 1, 'Enea': 3})

    app = Application(g)
    app.mainloop()
