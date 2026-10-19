from utils.distance import calculate_distance


def nearest_neighbor_solution(warehouse, vehicles, chemists):
    """
    Greedy Nearest Neighbor baseline.

    Starting from the warehouse, repeatedly selects the nearest
    unvisited chemist that can fit in the current vehicle.

    Once no remaining chemist can fit, the algorithm moves to
    the next vehicle.

    All chemists are assigned automatically.
    """

    remaining = {
        chemist["id"]: chemist
        for chemist in chemists
    }

    routes = [
        []
        for _ in vehicles
    ]

    loads = [
        0
        for _ in vehicles
    ]

    warehouse_location = (
        warehouse["x"],
        warehouse["y"]
    )

    # ---------------------------------------------------------
    # Process each vehicle
    # ---------------------------------------------------------

    for vehicle_index, vehicle in enumerate(vehicles):

        current_location = warehouse_location

        while remaining:

            feasible_chemists = []

            # Find all chemists that can fit in this vehicle
            for chemist_id, chemist in remaining.items():

                if (
                    loads[vehicle_index]
                    + chemist["demand"]
                    <= vehicle["capacity"]
                ):

                    distance = calculate_distance(
                        current_location,
                        (
                            chemist["x"],
                            chemist["y"]
                        )
                    )

                    feasible_chemists.append(
                        (
                            distance,
                            chemist_id
                        )
                    )

            # No chemist can fit in this vehicle
            if not feasible_chemists:
                break

            # Select nearest feasible chemist
            feasible_chemists.sort(
                key=lambda item: item[0]
            )

            _, selected_id = feasible_chemists[0]

            selected_chemist = remaining[selected_id]

            # Add chemist to route
            routes[vehicle_index].append(
                selected_id
            )

            # Update vehicle load
            loads[vehicle_index] += (
                selected_chemist["demand"]
            )

            # Move current location
            current_location = (
                selected_chemist["x"],
                selected_chemist["y"]
            )

            # Remove from unvisited set
            del remaining[selected_id]

    # ---------------------------------------------------------
    # If some chemists remain, assign them to the vehicle
    # with the lowest current load.
    #
    # This handles cases where total demand exceeds capacity
    # or an individual demand cannot fit normally.
    # ---------------------------------------------------------

    while remaining:

        selected_id = min(
            remaining,
            key=lambda chemist_id: calculate_distance(
                warehouse_location,
                (
                    remaining[chemist_id]["x"],
                    remaining[chemist_id]["y"]
                )
            )
        )

        selected_chemist = remaining[selected_id]

        vehicle_index = min(
            range(len(vehicles)),
            key=lambda index: loads[index]
        )

        routes[vehicle_index].append(
            selected_id
        )

        loads[vehicle_index] += (
            selected_chemist["demand"]
        )

        del remaining[selected_id]

    return routes