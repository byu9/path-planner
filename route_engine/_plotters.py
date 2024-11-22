from pprint import pformat

import folium

from gis_backend.query_provider import get_coord_of_node
from ._problem_description import VehicleRoutingProblemSolution


def _pretty_print_for_popup(obj):
    return pformat(obj, width=80)


def _get_coord_of_nodes(nodes):
    return [
        get_coord_of_node(node)
        for node in nodes
    ]


class RoutePlotter:

    @staticmethod
    def plot_solution_to_file(solution: VehicleRoutingProblemSolution, filename: str):
        problem = solution.problem
        folium_map = folium.Map(control_scale=True)

        # Plot waypoints
        for waypoint in problem.waypoints:
            waypoint_data = problem.waypoint(waypoint)
            folium.Marker(
                get_coord_of_node(waypoint_data.osm_node),
                popup=_pretty_print_for_popup(waypoint_data)
            ).add_to(folium_map)

        for vehicle in problem.vehicles:
            vehicle_layer = folium.FeatureGroup(name=f'{vehicle}').add_to(folium_map)

            # Plot trips of vehicle
            for activity in solution.trip_activity(vehicle):
                nodes = problem.trip_geometry(activity.trip)
                folium.PolyLine(
                    _get_coord_of_nodes(nodes),
                    popup=_pretty_print_for_popup(activity),
                    color='blue'
                ).add_to(vehicle_layer)

            # Plot dispatch and recall route of vehicle
            dispatch_activity = solution.dispatch_activity(vehicle)
            recall_activity = solution.recall_activity(vehicle)

            if dispatch_activity is not None:
                folium.Marker(
                    get_coord_of_node(dispatch_activity.from_osm_node),
                    tooltip='Dispatch facility',
                    icon=folium.Icon(icon='home'),
                    color='red',
                ).add_to(folium_map)

                nodes = problem.dispatch_geometry(vehicle, dispatch_activity.target_waypoint)
                folium.PolyLine(
                    _get_coord_of_nodes(nodes),
                    popup=_pretty_print_for_popup(dispatch_activity),
                    color='red'
                ).add_to(vehicle_layer)

            if recall_activity is not None:
                folium.Marker(
                    get_coord_of_node(recall_activity.to_osm_node),
                    tooltip='Recall facility',
                    icon=folium.Icon(icon='home'),
                    color='green',
                ).add_to(folium_map)

                nodes = problem.recall_geometry(vehicle, recall_activity.origin_waypoint)
                folium.PolyLine(
                    _get_coord_of_nodes(nodes),
                    popup=_pretty_print_for_popup(recall_activity),
                    color='green'
                ).add_to(vehicle_layer)

        folium.LayerControl(collapsed=False).add_to(folium_map)
        folium_map.fit_bounds(folium_map.get_bounds())
        folium_map.save(outfile=filename)
