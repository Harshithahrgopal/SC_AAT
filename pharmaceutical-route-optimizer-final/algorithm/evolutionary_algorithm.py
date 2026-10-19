# ============================================================
# EVOLUTIONARY ALGORITHM
# Pharmaceutical Delivery Route Optimization
# ============================================================

import random
from algorithm.baseline import nearest_neighbor_solution
from algorithm.fitness import (
    calculate_fitness
)


# ============================================================
# STEP 1: INITIAL POPULATION
# ============================================================

def generate_random_solution(
    chemists,
    num_vehicles
):

    chemist_ids = [
        chemist["id"]
        for chemist in chemists
    ]

    random.shuffle(
        chemist_ids
    )

    routes = [
        []
        for _ in range(num_vehicles)
    ]

    for index, chemist_id in enumerate(
        chemist_ids
    ):

        vehicle_index = (
            index % num_vehicles
        )

        routes[vehicle_index].append(
            chemist_id
        )

    return routes


def generate_nearby_solution(
    chemists,
    vehicles,
    warehouse
):
    """
    Create a capacity-feasible, geographically sensible initial solution.

    The chemists are first assigned to vehicles by searching for a
    capacity-feasible grouping with a small total nearest-neighbour
    travel distance. After assignment, each vehicle's chemists are
    ordered using nearest neighbour starting from the warehouse.

    This means the initial solution is not a random route: vehicles
    are grouped around nearby chemists while respecting capacity.
    """

    from utils.distance import calculate_distance

    chemist_lookup = {
        chemist["id"]: chemist
        for chemist in chemists
    }

    chemist_ids = [
        chemist["id"]
        for chemist in chemists
    ]

    warehouse_location = (
        warehouse["x"],
        warehouse["y"]
    )

    # --------------------------------------------------------
    # Find a capacity-feasible grouping with good geographic
    # locality. For the project's small demo dataset this exact
    # search is practical and avoids arbitrary vehicle assignment.
    # --------------------------------------------------------

    def nearest_neighbour_route(route_ids):
        remaining = set(route_ids)
        current_location = warehouse_location
        ordered = []
        distance = 0.0

        while remaining:
            nearest_id = min(
                remaining,
                key=lambda chemist_id: calculate_distance(
                    current_location,
                    (
                        chemist_lookup[chemist_id]["x"],
                        chemist_lookup[chemist_id]["y"]
                    )
                )
            )

            next_location = (
                chemist_lookup[nearest_id]["x"],
                chemist_lookup[nearest_id]["y"]
            )

            distance += calculate_distance(
                current_location,
                next_location
            )

            ordered.append(nearest_id)
            remaining.remove(nearest_id)
            current_location = next_location

        if ordered:
            distance += calculate_distance(
                current_location,
                warehouse_location
            )

        return distance, ordered

    # Vehicles are treated as interchangeable for the search, but
    # the final routes are returned in Vehicle 1, Vehicle 2, ... order.
    capacities = [
        vehicle["capacity"]
        for vehicle in vehicles
    ]

    best_routes = None
    best_distance = float("inf")
    routes = [[] for _ in vehicles]
    loads = [0 for _ in vehicles]

    # Put larger-demand chemists first during the search. This greatly
    # reduces unnecessary backtracking while the geographic score still
    # decides which feasible grouping is best.
    search_ids = sorted(
        chemist_ids,
        key=lambda chemist_id: chemist_lookup[chemist_id]["demand"],
        reverse=True
    )

    def search(index):
        nonlocal best_routes, best_distance

        if index == len(search_ids):
            total_distance = 0.0
            candidate_routes = []

            for route in routes:
                route_distance, ordered_route = nearest_neighbour_route(route)
                total_distance += route_distance
                candidate_routes.append(ordered_route)

            if total_distance < best_distance:
                best_distance = total_distance
                best_routes = [route.copy() for route in candidate_routes]

            return

        chemist_id = search_ids[index]
        demand = chemist_lookup[chemist_id]["demand"]

        for vehicle_index, capacity in enumerate(capacities):
            if loads[vehicle_index] + demand > capacity:
                continue

            routes[vehicle_index].append(chemist_id)
            loads[vehicle_index] += demand

            # Basic remaining-capacity pruning.
            remaining_demand = sum(
                chemist_lookup[search_ids[j]]["demand"]
                for j in range(index + 1, len(search_ids))
            )
            remaining_capacity = sum(
                capacities[j] - loads[j]
                for j in range(len(capacities))
            )

            if remaining_demand <= remaining_capacity:
                search(index + 1)

            loads[vehicle_index] -= demand
            routes[vehicle_index].pop()

    search(0)

    # Fallback for unusual inputs where no capacity-feasible solution
    # exists. The fitness function will report any resulting violation.
    if best_routes is None:
        routes = [[] for _ in vehicles]
        loads = [0 for _ in vehicles]

        for chemist in sorted(
            chemists,
            key=lambda item: item["demand"],
            reverse=True
        ):
            vehicle_index = min(
                range(len(vehicles)),
                key=lambda index: loads[index]
            )
            routes[vehicle_index].append(chemist["id"])
            loads[vehicle_index] += chemist["demand"]

        best_routes = []
        for route in routes:
            _, ordered_route = nearest_neighbour_route(route)
            best_routes.append(ordered_route)

    return best_routes


def generate_initial_population(
    chemists,
    vehicles,
    warehouse,
    population_size
):
    """
    Generate the initial population.

    The first individual is the Greedy Nearest Neighbor solution.
    The remaining individuals are generated using the existing
    nearby-solution logic so that the Evolutionary Algorithm
    starts from a meaningful baseline and still has diversity.
    """

    from algorithm.baseline import nearest_neighbor_solution

    population = []

    # ---------------------------------------------------------
    # First individual = Greedy Nearest Neighbor
    # ---------------------------------------------------------

    nn_solution = nearest_neighbor_solution(
        warehouse,
        vehicles,
        chemists
    )

    population.append(
        nn_solution
    )

    # ---------------------------------------------------------
    # Remaining individuals
    # ---------------------------------------------------------

    for _ in range(
        population_size - 1
    ):

        solution = generate_nearby_solution(
            chemists,
            vehicles,
            warehouse
        )

        population.append(
            solution
        )

    return population

# ============================================================
# STEP 2: TOURNAMENT SELECTION
# ============================================================

def tournament_selection(
    population,
    fitness_scores,
    tournament_size=3
):

    tournament_indices = random.sample(
        range(len(population)),
        min(
            tournament_size,
            len(population)
        )
    )

    best_index = (
        tournament_indices[0]
    )

    for index in tournament_indices[1:]:

        if (
            fitness_scores[index]
            <
            fitness_scores[best_index]
        ):

            best_index = index

    return population[
        best_index
    ]


def select_parents(
    population,
    fitness_scores,
    number_of_parents,
    tournament_size=3
):

    parents = []

    for _ in range(
        number_of_parents
    ):

        parent = tournament_selection(
            population,
            fitness_scores,
            tournament_size
        )

        parent_copy = [
            route.copy()
            for route in parent
        ]

        parents.append(
            parent_copy
        )

    return parents


# ============================================================
# STEP 3: FLATTEN ROUTES
# ============================================================

def flatten_solution(
    solution
):

    permutation = []

    for route in solution:

        permutation.extend(
            route
        )

    return permutation


# ============================================================
# STEP 4: GET ROUTE LENGTHS
# ============================================================

def get_route_lengths(
    solution
):

    return [
        len(route)
        for route in solution
    ]


# ============================================================
# STEP 5: ORDER CROSSOVER
# ============================================================

def order_crossover(
    parent1,
    parent2
):

    length = len(parent1)

    if length <= 1:

        return parent1.copy()

    point1, point2 = sorted(
        random.sample(
            range(length),
            2
        )
    )

    child = [
        None
    ] * length

    # Copy section from parent 1
    child[
        point1:point2 + 1
    ] = parent1[
        point1:point2 + 1
    ]

    used = set(
        child[
            point1:point2 + 1
        ]
    )

    # Remaining genes from parent 2
    parent2_items = [
        chemist
        for chemist in parent2
        if chemist not in used
    ]

    fill_positions = [
        index
        for index in range(length)
        if child[index] is None
    ]

    for position, chemist in zip(
        fill_positions,
        parent2_items
    ):

        child[
            position
        ] = chemist

    return child


# ============================================================
# STEP 6: SPLIT PERMUTATION INTO VEHICLE ROUTES
# ============================================================

def split_permutation(
    permutation,
    route_lengths
):

    routes = []

    start = 0

    for length in route_lengths:

        end = (
            start + length
        )

        route = permutation[
            start:end
        ]

        routes.append(
            route
        )

        start = end

    return routes


# ============================================================
# STEP 7: CROSSOVER
# ============================================================

def crossover(
    parent1,
    parent2,
    crossover_rate=0.8
):

    if random.random() > crossover_rate:

        child1 = [
            route.copy()
            for route in parent1
        ]

        child2 = [
            route.copy()
            for route in parent2
        ]

        return (
            child1,
            child2
        )

    permutation1 = (
        flatten_solution(
            parent1
        )
    )

    permutation2 = (
        flatten_solution(
            parent2
        )
    )

    child_permutation1 = (
        order_crossover(
            permutation1,
            permutation2
        )
    )

    child_permutation2 = (
        order_crossover(
            permutation2,
            permutation1
        )
    )

    route_lengths1 = (
        get_route_lengths(
            parent1
        )
    )

    route_lengths2 = (
        get_route_lengths(
            parent2
        )
    )

    child1 = split_permutation(
        child_permutation1,
        route_lengths1
    )

    child2 = split_permutation(
        child_permutation2,
        route_lengths2
    )

    return (
        child1,
        child2
    )


# ============================================================
# STEP 8: CROSSOVER FOR POPULATION
# ============================================================

def crossover_population(
    parents,
    crossover_rate=0.8
):

    children = []

    shuffled_parents = (
        parents.copy()
    )

    random.shuffle(
        shuffled_parents
    )

    for index in range(
        0,
        len(shuffled_parents) - 1,
        2
    ):

        parent1 = (
            shuffled_parents[index]
        )

        parent2 = (
            shuffled_parents[index + 1]
        )

        child1, child2 = (
            crossover(
                parent1,
                parent2,
                crossover_rate
            )
        )

        children.append(
            child1
        )

        children.append(
            child2
        )

    # Odd parent
    if len(shuffled_parents) % 2 == 1:

        last_parent = (
            shuffled_parents[-1]
        )

        last_parent_copy = [
            route.copy()
            for route in last_parent
        ]

        children.append(
            last_parent_copy
        )

    return children


# ============================================================
# STEP 9: SWAP MUTATION
# ============================================================

def swap_mutation(
    solution,
    mutation_rate=0.1
):

    mutated_solution = [
        route.copy()
        for route in solution
    ]

    if (
        random.random()
        >
        mutation_rate
    ):

        return mutated_solution

    all_chemists = (
        flatten_solution(
            mutated_solution
        )
    )

    if len(all_chemists) < 2:

        return mutated_solution

    index1, index2 = random.sample(
        range(
            len(all_chemists)
        ),
        2
    )

    # Swap two chemists
    (
        all_chemists[index1],
        all_chemists[index2]
    ) = (
        all_chemists[index2],
        all_chemists[index1]
    )

    route_lengths = (
        get_route_lengths(
            mutated_solution
        )
    )

    mutated_solution = (
        split_permutation(
            all_chemists,
            route_lengths
        )
    )

    return mutated_solution


# ============================================================
# STEP 10: MUTATION FOR POPULATION
# ============================================================

def mutate_population(
    population,
    mutation_rate=0.1
):

    mutated_population = []

    for solution in population:

        mutated_solution = (
            swap_mutation(
                solution,
                mutation_rate
            )
        )

        mutated_population.append(
            mutated_solution
        )

    return mutated_population


# ============================================================
# STEP 11: COMPLETE EVOLUTIONARY ALGORITHM
# ============================================================

def run_evolutionary_algorithm(
    chemists,
    vehicles,
    warehouse,
    population_size=50,
    generations=100,
    mutation_rate=0.1,
    crossover_rate=0.8,
    tournament_size=3
):

    # Initial population
    population = (
        generate_initial_population(
            chemists,
            vehicles,
            warehouse,
            population_size
        )
    )

    convergence_history = []

    best_solution = None

    best_result = None

    # --------------------------------------------------------
    # GENERATIONS
    # --------------------------------------------------------

    for generation in range(
        generations
    ):

        fitness_results = []

        # Evaluate population
        for solution in population:

            result = calculate_fitness(
                solution,
                warehouse,
                vehicles,
                chemists
            )

            fitness_results.append(
                result
            )

        fitness_scores = [
            result["fitness"]
            for result in fitness_results
        ]

        # Find best solution
        best_index = (
            fitness_scores.index(
                min(fitness_scores)
            )
        )

        current_best_solution = (
            population[
                best_index
            ]
        )

        current_best_result = (
            fitness_results[
                best_index
            ]
        )

        convergence_history.append(
            current_best_result[
                "fitness"
            ]
        )

        # Update global best
        if (
            best_result is None
            or
            current_best_result[
                "fitness"
            ]
            <
            best_result[
                "fitness"
            ]
        ):

            best_solution = [
                route.copy()
                for route in (
                    current_best_solution
                )
            ]

            best_result = (
                current_best_result.copy()
            )

        # Selection
        parents = select_parents(
            population,
            fitness_scores,
            population_size,
            tournament_size
        )

        # Crossover
        children = (
            crossover_population(
                parents,
                crossover_rate
            )
        )

        # Mutation
        children = (
            mutate_population(
                children,
                mutation_rate
            )
        )
        # ---------------------------------------------------------
        # ELITISM
        # Keep the best solution from the current generation
        # ---------------------------------------------------------

        elite_solution = [
            route.copy()
            for route in current_best_solution
        ]

        children.append(
            elite_solution
        )

        population = children

        # Maintain population size
        while len(population) < population_size:

            extra_solution = (
                generate_random_solution(
                    chemists,
                    len(vehicles)
                )
            )

            population.append(
                extra_solution
            )

        if len(population) > population_size:

            population = population[
                :population_size
            ]

    return {

        "best_solution":
            best_solution,

        "best_result":
            best_result,

        "convergence_history":
            convergence_history
    }


# ============================================================
# STEP 12: INITIAL VS OPTIMIZED COMPARISON
# ============================================================

def compare_initial_and_optimized(
    chemists,
    vehicles,
    warehouse,
    optimized_result
):

    # --------------------------------------------------------
    # Generate nearby initial solution
    # --------------------------------------------------------

    initial_solution = nearest_neighbor_solution(
    warehouse,
    vehicles,
    chemists
)

    # Evaluate initial solution
    initial_result = calculate_fitness(
        initial_solution,
        warehouse,
        vehicles,
        chemists
    )

    # --------------------------------------------------------
    # Get optimized solution
    # --------------------------------------------------------

    optimized_solution = (
        optimized_result[
            "best_solution"
        ]
    )

    optimized_result_data = (
        calculate_fitness(
            optimized_solution,
            warehouse,
            vehicles,
            chemists
        )
    )

    # --------------------------------------------------------
    # Distance improvement
    # --------------------------------------------------------

    distance_improvement = (
        initial_result[
            "total_distance"
        ]
        -
        optimized_result_data[
            "total_distance"
        ]
    )

    if initial_result[
        "total_distance"
    ] > 0:

        distance_improvement_percentage = (
            distance_improvement
            /
            initial_result[
                "total_distance"
            ]
        ) * 100

    else:

        distance_improvement_percentage = 0

    # --------------------------------------------------------
    # Fitness improvement
    # --------------------------------------------------------

    fitness_improvement = (
        initial_result[
            "fitness"
        ]
        -
        optimized_result_data[
            "fitness"
        ]
    )

    if initial_result[
        "fitness"
    ] > 0:

        fitness_improvement_percentage = (
            fitness_improvement
            /
            initial_result[
                "fitness"
            ]
        ) * 100

    else:

        fitness_improvement_percentage = 0

    # --------------------------------------------------------
    # Vehicle-wise comparison
    # --------------------------------------------------------

    route_comparison = []

    for index, vehicle in enumerate(
        vehicles
    ):

        initial_route = (
            initial_solution[index]
        )

        optimized_route = (
            optimized_solution[index]
        )

        route_comparison.append(
            {
                "vehicle":
                    vehicle["id"],

                "initial_route":
                    initial_route,

                "optimized_route":
                    optimized_route,

                "initial_load":
                    initial_result[
                        "route_details"
                    ][index]["load"],

                "optimized_load":
                    optimized_result_data[
                        "route_details"
                    ][index]["load"],

                "initial_late":
                    initial_result[
                        "route_details"
                    ][index]["late_minutes"],

                "optimized_late":
                    optimized_result_data[
                        "route_details"
                    ][index]["late_minutes"]
            }
        )

    return {

        "initial_solution":
            initial_solution,

        "initial_result":
            initial_result,

        "optimized_solution":
            optimized_solution,

        "optimized_result":
            optimized_result_data,

        "route_comparison":
            route_comparison,

        "distance_improvement":
            distance_improvement,

        "distance_improvement_percentage":
            distance_improvement_percentage,

        "fitness_improvement":
            fitness_improvement,

        "fitness_improvement_percentage":
            fitness_improvement_percentage
    }