import gis_backend.map_viewer as plt
from gis_backend.query_provider import get_node_at_address
from gis_backend.query_provider import get_path_metric
from gis_backend.query_provider import get_shortest_path_between

waypoints = [
    '715 Nazareth St, Raleigh, NC 27606',
    '1240 Farmers Market Dr, Raleigh, NC 27606',
    '500 S Salisbury St, Raleigh, NC 27601',
    '300 New Bern Ave, Raleigh NC 27610',
    '2500 Glenwood Ave, Raleigh NC 27608'
]

node0 = get_node_at_address(waypoints[0])
node1 = get_node_at_address(waypoints[1])

path = get_shortest_path_between(node0, node1)
print(path)
print(get_path_metric(path, metric='length'))

fig = plt.figure()
fig.plot_path(path)
plt.show()
