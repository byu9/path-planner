from argparse import ArgumentParser

from ._osmnx_wrapper import ox
from ._pickling import save_object

parser = ArgumentParser(description='Fetch OSM map data')
parser.add_argument('--fetch-place', type=str, required=True)
args = parser.parse_args()

# See https://wiki.openstreetmap.org/wiki/Key:highway
include_highways = [
    'motorway',
    'trunk',
    'primary',
    'secondary',
    'tertiary',
    'unclassified',
    'residential',
    'motorway_link',
    'trunk_link',
    'primary_link',
    'secondary_link',
    'tertiary_link',
    'living_street',
    'service',
]

# Uses the OSM overpass query syntax
# https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#The_Query_Filter
custom_filter = '["highway"~"' + '|'.join(include_highways) + '"]'

graph = ox.graph_from_place(
    args.fetch_place,
    retain_all=True,
    truncate_by_edge=True,
    custom_filter=custom_filter,
    simplify=False
)

graph = ox.add_edge_speeds(graph)
graph = ox.add_edge_travel_times(graph)

nodes, edges = ox.graph_to_gdfs(graph)

save_object(graph, 'gis_data/graph.pickle')
save_object(nodes, 'gis_data/nodes.pickle')
save_object(edges, 'gis_data/edges.pickle')
