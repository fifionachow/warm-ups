import networkx as nx

def draw_graph(edge_df, node_df, weight='walking', directed=False):
    # Create empty graph
    if directed:
        g = nx.DiGraph()
    else:
        g = nx.Graph()

    edge_col = edge_df.columns
    node_col = node_df.columns

    # Add edges and edge attributes
    for i, elrow in edge_df.iterrows():
        edge_dict = dict(zip(edge_col, elrow))
        g.add_edge(edge_dict['from'], edge_dict['to'], attr_dict=edge_dict, weight=edge_dict[weight])

    for i, nlrow in node_df.iterrows():
        node_dict = dict(zip(node_col, nlrow))
        g.node[node_dict['index']].update(node_dict)
    return g