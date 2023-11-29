''' Minimum Spanning Tree (MST) for Portfolio Diversification '''


class Node:
    def __init__(self, node_name):
        self._node_name = node_name
        self._neighbors = []

    def add_neighbor(self, node_name, neighbour_node_name, edge_value):
        self._neighbors.append((node_name, neighbour_node_name, edge_value))

    def get_neighbors(self):
        return self._neighbors


class Graph:
    def __init__(self, node_names):
        self._nodes = {}
        self._node_names = node_names

    def create_graph(self, correlation_matrix):
        for i, row in enumerate(correlation_matrix):
            node = Node(self._node_names[i])
            for j, edge_value in enumerate(row):
                if i != j:
                    node.add_neighbor(self._node_names[i], self._node_names[j], edge_value)
            self._nodes[self._node_names[i]] = node

    def get_node(self, node_name: str) -> Node:
        return self._nodes.get(node_name)

    def get_nodes(self):
        return self._nodes

    def get_nodes_names(self):
        return self._node_names


class MinimumSpanningTree:
    def __init__(self, graph):
        self._graph = graph
        self._forest = []
        self._included_nodes = []

    def minimum_cost_neighbor(self, neighbors):
        abs_min_cost = min(abs(neighbor[2]) for neighbor in neighbors)
        for neighbor in neighbors:
            if abs(neighbor[2]) == abs_min_cost:
                min_cost_neighbor = neighbor
                return min_cost_neighbor

    def calculate_cost(self):
        node_names = graph.get_nodes_names()
        self._included_nodes.append("E")
        while len(self._included_nodes) < len(node_names):
            tree_neighbors = []
            for included_node_name in self._included_nodes:
                included_node = graph.get_node(included_node_name)
                node_neighbors = included_node.get_neighbors()
                tree_neighbors.extend(node_neighbors)
            while len(tree_neighbors)>0:
                min_cost_neighbor = self.minimum_cost_neighbor(tree_neighbors)
                if not min_cost_neighbor[1] in self._included_nodes:
                    self._included_nodes.append(min_cost_neighbor[1])
                    self._forest.append(min_cost_neighbor)
                    break
                tree_neighbors.remove(min_cost_neighbor)

    def get_forest(self):
        return self._forest


class PortfolioDiversification:
    def __init__(self, forest, total_investment):
        self._forest = forest
        self._weights = {}
        self._investment_alocation = {}
        self._total_investment = total_investment

    def allocate_invesments(self):
        for edge in self._forest:
            asset1, asset2, weight = edge[0],edge[1], edge[2]
            if asset1 in self._weights:
                self._weights[asset1] += abs(1/weight)
            else:
                self._weights[asset1] = abs(1/weight)
            if asset2 in self._weights:
                self._weights[asset2] += abs(1/weight)
            else:
                self._weights[asset2] = abs(1/weight)
        total_weight = sum(self._weights.values())
        self._investment_alocation = {asset: self._total_investment * weight / total_weight 
                                      for asset, weight in self._weights.items()}

    def get_investment_allocation(self):
        return self._investment_alocation

    def get_asset_weights(self):
        return self._weights


# Example
correlation_matrix = [
    [1.0, 0.6, -0.2, 0.1, 0.4],
    [0.6, 1.0, 0.3, -0.1, 0.7],
    [-0.2, 0.3, 1.0, 0.4, -0.2],
    [0.1, -0.1, 0.4, 1.0, 0.5],
    [0.4, 0.7, -0.2, 0.5, 1.0]
]

node_names = ['A', 'B', 'C', 'D', 'E']

total_investment = 10000


graph = Graph(node_names)
graph.create_graph(correlation_matrix)

mst = MinimumSpanningTree(graph)
mst.calculate_cost()
forest = mst.get_forest()

pd = PortfolioDiversification(forest, total_investment)
pd.allocate_invesments()
investment_allocation = pd.get_investment_allocation()
asset_weights = pd.get_asset_weights()


print(f"Forest: {forest}")
print(f"Asset weights: {asset_weights}")
print(f"Investment allocation: {investment_allocation}")