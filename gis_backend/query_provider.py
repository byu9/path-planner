import geopandas as gpd

_nodes = gpd.read_file('gis_database/simplified_nodes.geojson')
_edges = gpd.read_file('gis_database/simplified_edges.geojson')


def find_edge_geometry(u, v, key=0):
    rows = (
        (_edges['u'] == u) &
        (_edges['v'] == v) &
        (_edges['key'] == key)
    )
    return _edges[rows]
