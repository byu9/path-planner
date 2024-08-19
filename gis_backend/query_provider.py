from ._osmnx_wrapper import ox
import osmnx.routing as ox_routing
import osmnx.utils_graph as ox_utils_graph

from ._pickling import load_object

_graph = load_object('gis_data/graph.pickle')
_nodes = load_object('gis_data/nodes.pickle')
_edges = load_object('gis_data/edges.pickle')


def get_node_at_address(address):
    lat, long = ox.geocode(address)
    return ox.nearest_nodes(_graph, X=long, Y=lat)


def get_node_geometry(node):
    point = _nodes['geometry'][node]
    return point.y, point.x


def get_shortest_path_between(src_node, dst_node):
    return ox_routing.shortest_path(_graph, src_node, dst_node)


def get_path_metric(path, metric='length'):
    gdf = ox_utils_graph.route_to_gdf(_graph, path, weight=metric)
    return gdf['length'].sum()
