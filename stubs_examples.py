import gis_backend.map_viewer as plt
from gis_backend.query_provider import get_node_at_address
from gis_backend.query_provider import get_node_geometry
from gis_backend.query_provider import get_path_metric
from gis_backend.query_provider import get_shortest_path_between

address1 = '11 W Jones St, Raleigh NC 27601'
address2 = '2409 Crabtree Blvd, Raleigh NC 27604'

# Uses the geocoding service from OSM
node1 = get_node_at_address(address1)
node2 = get_node_at_address(address2)

# Returns the longitude and latitude
coord1 = get_node_geometry(node1)
coord2 = get_node_geometry(node2)

print(f'Location of {address1}: {coord1}')
print(f'Location of {address2}: {coord2}')

# Uses the shortest path from OSMNX (NetworkX Dijkstra)
path = get_shortest_path_between(node1, node2)
distance = get_path_metric(path)

print(f'Shortest path between {address1} {address2}: {path}')
print(f'Shortest path distance {distance}')

fig = plt.figure()
fig.plot_node(node1)
fig.plot_node(node2)
fig.plot_path(path)
plt.show()
