import osmnx as ox

ox.settings.cache_folder = 'osmnx_cache'
ox.settings.log_console = True

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

graph = ox.graph_from_address(
    'North Carolina State University',
    retain_all=True,
    truncate_by_edge=True,
    custom_filter=custom_filter
)

nodes, edges = ox.graph_to_gdfs(graph, nodes=True, edges=True,
                                fill_edge_geometry=True)

nodes.drop(columns=['highway', 'street_count', 'x', 'y'], errors='ignore',
           inplace=True)
edges.drop(columns=[
    'access', 'lanes', 'service', 'ref', 'bridge', 'width', 'junction',
    'tunnel', 'reversed', 'name', 'highway', 'oneway',
], errors='ignore', inplace=True)

nodes.to_file('gis_database/simplified_nodes.geojson', driver='GeoJSON')
edges.to_file('gis_database/simplified_edges.geojson', driver='GeoJSON')
