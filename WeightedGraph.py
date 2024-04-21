class WeightedGraph:
    def __init__(self):
        self.graph = {}

    def add_path(self, nodes, id):
        if id not in self.graph:
            self.graph[id] = {'neighbors': set(), 'attributes': {}}
        self.graph[id]['neighbors'].update(nodes)

    def add_weighted_edges_from(self, weighted_edges, weight):
        for edge in weighted_edges:
            u, v, w = edge
            if u in self.graph and v in self.graph:
                self.graph[u]['neighbors'].add(v)
                self.graph[v]['neighbors'].add(u)
                self.graph[u]['attributes'].setdefault(v, {})[weight] = w
                self.graph[v]['attributes'].setdefault(u, {})[weight] = w

    def nodes_iter(self):
        return iter(self.graph.keys())

    def edges_iter(self, data=False):
        for u, neighbors_data in self.graph.items():
            for v in neighbors_data['neighbors']:
                if data:
                    yield u, v, neighbors_data['attributes'].get(v, {})
                else:
                    yield u, v

    def node(self, node_id):
        node_data = self.graph.get(node_id)
        if node_data is not None:
            return node_data.get('attributes', {'lon': None, 'lat': None})
        else:
            return {'lon': None, 'lat': None}  # Return default values if node not found


    def add_node(self, node_id, attrs):
        self.graph[node_id] = {'neighbors': set(), 'attributes': attrs}

    def add_edge(self, u, v, attrs):
        if u not in self.graph:
            self.graph[u] = {'neighbors': set(), 'attributes': {}}
        if v not in self.graph:
            self.graph[v] = {'neighbors': set(), 'attributes': {}}
        self.graph[u]['neighbors'].add(v)
        self.graph[v]['neighbors'].add(u)
        self.graph[u]['attributes'].setdefault(v, {}).update(attrs)
        self.graph[v]['attributes'].setdefault(u, {}).update(attrs)

    def clear(self):
        self.graph = {}

    def __getitem__(self, item):
        return self.graph[item]

    def __str__(self):
        return str(self.graph)
