import osmnx.routing as ox_routing

from ._osmnx_wrapper import ox
from ._pickling import load_object

_graph = load_object('gis_data/graph.pickle')
_nodes = load_object('gis_data/nodes.pickle')
_edges = load_object('gis_data/edges.pickle')


def get_node_near_coord(lat, long):
    return ox.nearest_nodes(_graph, X=long, Y=lat)


def get_node_near_address(address):
    lat, long = ox.geocode(address)
    return get_node_near_coord(lat=lat, long=long)


def get_coord_of_node(node):
    point = _nodes['geometry'][node]
    lat = point.y
    long = point.x
    return lat, long


def get_shortest_path_between(src_node, dst_node, metric='length'):
    return ox_routing.shortest_path(_graph, src_node, dst_node, weight=metric)


def get_path_metric(path, metric='length'):
    assert metric in ['length', 'travel_time']

    gdf = ox_routing.route_to_gdf(_graph, path, weight=metric)
    return gdf[metric].sum()
