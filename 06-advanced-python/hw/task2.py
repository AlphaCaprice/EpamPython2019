"""
E - dict(<V> : [<V>, <V>, ...])
Ключ - строка, идентифицирующая вершину графа
значение - список вершин, достижимых из данной

Сделать так, чтобы по графу можно было итерироваться(обходом в ширину)

"""


class Graph:
    def __init__(self, g: dict):
        self.g = g

    def __iter__(self):
        return GraphIterator(self.g)


class GraphIterator:
    def __init__(self, graph):
        self.g_iterable = self.__get_bfs_graph(graph)
        self._cursor = -1

    @staticmethod
    def __get_bfs_graph(g):
        def get_next(vertex):
            for edge in g[vertex]:
                if edge not in visited:
                    visited.add(edge)
                    vertices_bfs.append(edge)
                    need_to_visit.append(edge)
            while need_to_visit:
                get_next(need_to_visit.pop(0))

        vertices_bfs = []
        root = list(g.keys())[0]
        visited = {root}
        need_to_visit = []
        vertices_bfs.append(root)
        get_next(root)
        return vertices_bfs

    def __next__(self):
        self._cursor += 1
        if self._cursor >= len(self.g_iterable):
            raise StopIteration()
        return self.g_iterable[self._cursor]


E = {'A': ['B', 'C', 'D'], 'C': ['F'], 'D': ['A'], 'E': ['F'],
     'F': ['G'], 'G': [], 'B': ['C', 'E']}
graph = Graph(E)


for vertex in graph:
    print(vertex)
