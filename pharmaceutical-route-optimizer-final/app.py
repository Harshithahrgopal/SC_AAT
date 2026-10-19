# ============================================================
# PHARMA ROUTE AI
# Pharmaceutical Delivery Route Optimization
# Evolutionary Algorithm
# ============================================================

import streamlit as st
import matplotlib.pyplot as plt
from algorithm.baseline import nearest_neighbor_solution
from algorithm.fitness import calculate_fitness
from data.sample_data import (
    WAREHOUSE,
    VEHICLES,
    CHEMISTS
)

from algorithm.evolutionary_algorithm import (
    run_evolutionary_algorithm,
    compare_initial_and_optimized
)

from algorithm.testing import (
    run_test_cases
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PharmaRoute AI",
    page_icon="💊",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "💊 PharmaRoute AI"
)

st.subheader(
    "Pharmaceutical Delivery Route Optimization "
    "Using Evolutionary Algorithm"
)

st.write(
    "Optimize medicine delivery routes from a "
    "central pharmaceutical warehouse to multiple "
    "chemists while considering vehicle capacity, "
    "delivery time windows and travel distance."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "⚙️ Evolutionary Algorithm Settings"
)

population_size = st.sidebar.slider(
    "Population Size",
    min_value=10,
    max_value=200,
    value=50,
    step=10
)

generations = st.sidebar.slider(
    "Generations",
    min_value=10,
    max_value=500,
    value=100,
    step=10
)

mutation_rate = st.sidebar.slider(
    "Mutation Rate",
    min_value=0.0,
    max_value=1.0,
    value=0.10,
    step=0.05
)

crossover_rate = st.sidebar.slider(
    "Crossover Rate",
    min_value=0.0,
    max_value=1.0,
    value=0.80,
    step=0.05
)

tournament_size = st.sidebar.slider(
    "Tournament Size",
    min_value=2,
    max_value=10,
    value=3,
    step=1
)


# ============================================================
# PROJECT OVERVIEW
# ============================================================

st.header(
    "📌 Problem Overview"
)

overview_col1, overview_col2, overview_col3 = (
    st.columns(3)
)

with overview_col1:

    st.metric(
        "Chemists",
        len(CHEMISTS)
    )

with overview_col2:

    st.metric(
        "Vehicles",
        len(VEHICLES)
    )

with overview_col3:

    st.metric(
        "Optimization Method",
        "Evolutionary Algorithm"
    )


# ============================================================
# HOW SYSTEM WORKS
# ============================================================

st.header(
    "🔄 How the System Works"
)

step1, step2, step3, step4, step5 = (
    st.columns(5)
)

with step1:
    st.write("### 1️⃣")
    st.write("Generate")
    st.caption(
        "Create initial delivery routes"
    )

with step2:
    st.write("### 2️⃣")
    st.write("Evaluate")
    st.caption(
        "Calculate route fitness"
    )

with step3:
    st.write("### 3️⃣")
    st.write("Select")
    st.caption(
        "Choose better solutions"
    )

with step4:
    st.write("### 4️⃣")
    st.write("Evolve")
    st.caption(
        "Crossover + mutation"
    )

with step5:
    st.write("### 5️⃣")
    st.write("Optimize")
    st.caption(
        "Find best delivery routes"
    )


# ============================================================
# NETWORK STATISTICS
# ============================================================

st.header(
    "📍 Delivery Network"
)

network_col1, network_col2, network_col3 = (
    st.columns(3)
)

with network_col1:

    st.metric(
        "Warehouse",
        WAREHOUSE["id"]
    )

with network_col2:

    total_demand = sum(
        chemist["demand"]
        for chemist in CHEMISTS
    )

    st.metric(
        "Total Medicine Demand",
        total_demand
    )

with network_col3:

    total_capacity = sum(
        vehicle["capacity"]
        for vehicle in VEHICLES
    )

    st.metric(
        "Fleet Capacity",
        total_capacity
    )


# ============================================================
# NETWORK VISUALIZATION
# ============================================================

st.header(
    "🗺️ Delivery Network Map"
)

fig, ax = plt.subplots(
    figsize=(10, 6)
)

# Warehouse
ax.scatter(
    WAREHOUSE["x"],
    WAREHOUSE["y"],
    s=250,
    marker="s"
)

ax.annotate(
    "Warehouse",
    (
        WAREHOUSE["x"],
        WAREHOUSE["y"]
    ),
    xytext=(8, 8),
    textcoords="offset points"
)

# Chemists
for chemist in CHEMISTS:

    ax.scatter(
        chemist["x"],
        chemist["y"],
        s=120
    )

    ax.annotate(
        chemist["id"],
        (
            chemist["x"],
            chemist["y"]
        ),
        xytext=(6, 6),
        textcoords="offset points"
    )

ax.set_xlabel(
    "X Coordinate"
)

ax.set_ylabel(
    "Y Coordinate"
)

ax.set_title(
    "Warehouse and Chemist Locations"
)

ax.grid(
    True,
    alpha=0.3
)

st.pyplot(
    fig
)

plt.close(fig)


# ============================================================
# CHEMIST INFORMATION
# ============================================================

st.header(
    "🏪 Chemist Requirements"
)

chemist_table = []

for chemist in CHEMISTS:

    chemist_table.append(
        {
            "Chemist":
                chemist["id"],

            "Location":
                f"({chemist['x']}, {chemist['y']})",

            "Demand":
                chemist["demand"],

            "Time Window":
                f"{chemist['time_window'][0]:02d}:00 - "
                f"{chemist['time_window'][1]:02d}:00"
        }
    )

st.dataframe(
    chemist_table,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# VEHICLE INFORMATION
# ============================================================

st.header(
    "🚚 Vehicle Fleet"
)

vehicle_table = []

for vehicle in VEHICLES:

    vehicle_table.append(
        {
            "Vehicle":
                vehicle["id"],

            "Capacity":
                vehicle["capacity"],

            "Starting Point":
                "Warehouse",

            "Return Point":
                "Warehouse"
        }
    )

st.dataframe(
    vehicle_table,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# CONSTRAINTS
# ============================================================

st.header(
    "⚖️ Optimization Constraints"
)

constraint1, constraint2, constraint3 = (
    st.columns(3)
)

with constraint1:

    st.write(
        "### 📦 Capacity"
    )

    st.write(
        "Each vehicle has a maximum medicine "
        "carrying capacity."
    )

with constraint2:

    st.write(
        "### ⏰ Time Windows"
    )

    st.write(
        "Each chemist has a permitted delivery "
        "time window."
    )

with constraint3:

    st.write(
        "### 📏 Distance"
    )

    st.write(
        "The algorithm attempts to minimize "
        "total travel distance."
    )

# ========================================================
# OBJECTIVE FORMULA
# ========================================================

st.header(
    "🧮 Optimization Objective"
)

# Basic fitness formula
st.latex(
    r"""
    \text{Fitness} =
    \text{Total Distance}
    +
    \text{Capacity Penalty}
    +
    \text{Time Window Penalty}
    """
)

st.write(
    "The Evolutionary Algorithm attempts to minimize this fitness value. "
    "A lower fitness value represents a better delivery solution."
)

# Detailed fitness calculation
st.subheader("Detailed Fitness Calculation")

st.latex(
    r"""
    \text{Fitness} =
    \text{Total Distance}
    +
    (\text{Capacity Violation} \times 1000)
    +
    (\text{Late Minutes} \times 10)
    """
)

st.write(
    "Capacity Penalty = Capacity Violation × 1000"
)

st.write(
    "Time Window Penalty = Late Minutes × 10"
)

st.write(
    "The capacity penalty is given a high weight of 1000 to strongly "
    "discourage vehicles from exceeding their capacity. Late deliveries "
    "are penalized by 10 for every late minute. Therefore, the algorithm "
    "tries to minimize distance while maintaining vehicle capacity and "
    "meeting delivery time windows."
)
# ============================================================
# EA CONFIGURATION
# ============================================================

st.header(
    "🧬 Evolutionary Algorithm Configuration"
)

configuration_table = [
    {
        "Parameter":
            "Population Size",

        "Value":
            population_size
    },

    {
        "Parameter":
            "Generations",

        "Value":
            generations
    },

    {
        "Parameter":
            "Mutation Rate",

        "Value":
            mutation_rate
    },

    {
        "Parameter":
            "Crossover Rate",

        "Value":
            crossover_rate
    },

    {
        "Parameter":
            "Tournament Size",

        "Value":
            tournament_size
    }
]

st.dataframe(
    configuration_table,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# OPTIMIZATION BUTTON
# ============================================================

st.divider()

run_button = st.button(
    "🚚 FIND THE BEST DELIVERY ROUTES",
    type="primary",
    use_container_width=True
)


# ============================================================
# RUN OPTIMIZATION
# ============================================================

if run_button:

    with st.spinner(
        "Running Evolutionary Algorithm..."
    ):

        result = run_evolutionary_algorithm(
            chemists=CHEMISTS,

            vehicles=VEHICLES,

            warehouse=WAREHOUSE,

            population_size=
                population_size,

            generations=
                generations,

            mutation_rate=
                mutation_rate,

            crossover_rate=
                crossover_rate,

            tournament_size=
                tournament_size
        )

    st.success(
        "Optimization completed successfully!"
    )


    # ========================================================
    # GET RESULTS
    # ========================================================

    best_solution = (
        result["best_solution"]
    )

    best_result = (
        result["best_result"]
    )

    convergence_history = (
        result["convergence_history"]
    )


    # ========================================================
    # OPTIMIZED DELIVERY SUMMARY
    # ========================================================

    st.header(
        "🏆 Optimized Delivery Summary"
    )

    summary_col1, summary_col2, summary_col3, summary_col4 = (
        st.columns(4)
    )

    with summary_col1:

        st.metric(
            "Total Distance",
            f"{best_result['total_distance']:.2f}"
        )

    with summary_col2:

        st.metric(
            "Fitness",
            f"{best_result['fitness']:.2f}"
        )

    with summary_col3:

        st.metric(
            "Capacity Violation",
            f"{best_result['capacity_violation']:.2f}"
        )

    with summary_col4:

        st.metric(
            "Late Minutes",
            f"{best_result['late_minutes']:.2f}"
        )


    # ========================================================
    # VEHICLE-WISE ROUTES
    # ========================================================

    st.header(
        "🚚 Optimized Vehicle Routes"
    )

    for index, route in enumerate(
        best_solution
    ):

        vehicle = VEHICLES[index]

        route_text = " → ".join(
            ["Warehouse"]
            + route
            + ["Warehouse"]
        )

        st.subheader(
            f"🚚 {vehicle['id']}"
        )

        st.success(
            route_text
        )

        route_info = (
            best_result[
                "route_details"
            ][index]
        )

        route_col1, route_col2, route_col3 = (
            st.columns(3)
        )

        with route_col1:

            st.metric(
                "Medicine Load",
                route_info["load"]
            )

        with route_col2:

            st.metric(
                "Vehicle Capacity",
                route_info["capacity"]
            )

        with route_col3:

            st.metric(
                "Late Minutes",
                f"{route_info['late_minutes']:.2f}"
            )


    # ========================================================
    # CONSTRAINT STATUS
    # ========================================================

    st.header(
        "⚖️ Constraint Status"
    )

    if best_result[
        "capacity_violation"
    ] == 0:

        st.success(
            "✅ All vehicle capacity constraints "
            "are satisfied."
        )

    else:

        st.warning(
            f"⚠️ Capacity violation: "
            f"{best_result['capacity_violation']:.2f}"
        )

    if best_result[
        "late_minutes"
    ] == 0:

        st.success(
            "✅ All delivery time windows "
            "are satisfied."
        )

    else:

        st.warning(
            f"⚠️ Total late minutes: "
            f"{best_result['late_minutes']:.2f}"
        )


    # ========================================================
    # CONVERGENCE GRAPH
    # ========================================================

    st.header(
        "📈 Evolutionary Algorithm Convergence"
    )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.plot(
        range(
            1,
            len(convergence_history) + 1
        ),
        convergence_history
    )

    ax.set_xlabel(
        "Generation"
    )

    ax.set_ylabel(
        "Best Fitness"
    )

    ax.set_title(
        "Fitness Convergence Across Generations"
    )

    ax.grid(
        True,
        alpha=0.3
    )

    st.pyplot(
        fig
    )

    plt.close(fig)


    # ========================================================
    # FITNESS BREAKDOWN
    # ========================================================

    st.header(
        "🧮 Fitness Breakdown"
    )

    fitness_table = [
        {
            "Component":
                "Travel Distance",

            "Value":
                round(
                    best_result[
                        "total_distance"
                    ],
                    2
                )
        },

        {
            "Component":
                "Capacity Penalty",

            "Value":
                round(
                    best_result[
                        "capacity_penalty"
                    ],
                    2
                )
        },

        {
            "Component":
                "Time Window Penalty",

            "Value":
                round(
                    best_result[
                        "time_penalty"
                    ],
                    2
                )
        },

        {
            "Component":
                "Total Fitness",

            "Value":
                round(
                    best_result[
                        "fitness"
                    ],
                    2
                )
        }
    ]

    st.dataframe(
        fitness_table,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # ARRIVAL DETAILS
    # ========================================================

    st.header(
        "⏰ Delivery Arrival Details"
    )

    arrival_table = []

    for route_detail in (
        best_result[
            "route_details"
        ]
    ):

        for arrival in (
            route_detail[
                "arrivals"
            ]
        ):

            total_minutes = (
                arrival[
                    "arrival_time"
                ]
            )

            hours = int(
                total_minutes // 60
            )

            minutes = int(
                total_minutes % 60
            )

            arrival_table.append(
                {
                    "Vehicle":
                        route_detail[
                            "vehicle"
                        ],

                    "Chemist":
                        arrival[
                            "chemist"
                        ],

                    "Arrival Time":
                        f"{hours:02d}:{minutes:02d}",

                    "Late Minutes":
                        round(
                            arrival[
                                "late_minutes"
                            ],
                            2
                        )
                }
            )

    st.dataframe(
        arrival_table,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # OPTIMIZED ROUTE MAP
    # ========================================================

    st.header(
        "🗺️ Optimized Route Map"
    )

    fig, ax = plt.subplots(
        figsize=(11, 7)
    )

    # Warehouse
    ax.scatter(
        WAREHOUSE["x"],
        WAREHOUSE["y"],
        s=300,
        marker="s"
    )

    ax.annotate(
        "Warehouse",
        (
            WAREHOUSE["x"],
            WAREHOUSE["y"]
        ),
        xytext=(8, 8),
        textcoords="offset points"
    )

    chemist_lookup = {
        chemist["id"]: chemist
        for chemist in CHEMISTS
    }

    for chemist in CHEMISTS:

        ax.scatter(
            chemist["x"],
            chemist["y"],
            s=100
        )

        ax.annotate(
            chemist["id"],
            (
                chemist["x"],
                chemist["y"]
            ),
            xytext=(6, 6),
            textcoords="offset points"
        )

    # Draw each optimized route
    for index, route in enumerate(
        best_solution
    ):

        points = [
            (
                WAREHOUSE["x"],
                WAREHOUSE["y"]
            )
        ]

        for chemist_id in route:

            chemist = (
                chemist_lookup[
                    chemist_id
                ]
            )

            points.append(
                (
                    chemist["x"],
                    chemist["y"]
                )
            )

        points.append(
            (
                WAREHOUSE["x"],
                WAREHOUSE["y"]
            )
        )

        x_values = [
            point[0]
            for point in points
        ]

        y_values = [
            point[1]
            for point in points
        ]

        ax.plot(
            x_values,
            y_values,
            marker="o",
            label=VEHICLES[
                index
            ]["id"]
        )

    ax.set_xlabel(
        "X Coordinate"
    )

    ax.set_ylabel(
        "Y Coordinate"
    )

    ax.set_title(
        "Optimized Pharmaceutical Delivery Routes"
    )

    ax.legend()

    ax.grid(
        True,
        alpha=0.3
    )

    st.pyplot(
        fig
    )

    plt.close(fig)


    # ========================================================
    # INITIAL VS OPTIMIZED COMPARISON
    # ========================================================

    comparison = (
        compare_initial_and_optimized(
            chemists=CHEMISTS,
            vehicles=VEHICLES,
            warehouse=WAREHOUSE,
            optimized_result=result
        )
    )

    st.divider()

    st.header(
        "📉 Initial vs Optimized Solution"
    )

    st.write(
        "The Evolutionary Algorithm starts with an "
        "initial random delivery order and searches "
        "for a better arrangement of chemist visits."
    )
# --------------------------------------------------------
    # Nearest Neighbor vs Evolutionary Algorithm
    # --------------------------------------------------------

    st.divider()

    st.header(
        "🤝 Nearest Neighbor vs Evolutionary Algorithm"
    )

    st.write(
        "Nearest Neighbor is used as a greedy baseline. "
        "Both approaches are evaluated using the same "
        "delivery data and constraints."
    )

    # --------------------------------------------------------
    # Chemist Visiting Order
    # --------------------------------------------------------

    st.subheader(
        "Chemist Visiting Order"
    )

    st.write(
        "The following comparison shows exactly how "
        "the visiting sequence changed for each vehicle."
    )

    for route_data in (
        comparison[
            "route_comparison"
        ]
    ):

        vehicle_id = (
            route_data[
                "vehicle"
            ]
        )

        initial_route = (
            route_data[
                "initial_route"
            ]
        )

        optimized_route = (
            route_data[
                "optimized_route"
            ]
        )

        initial_text = " → ".join(
            ["Warehouse"]
            + initial_route
            + ["Warehouse"]
        )

        optimized_text = " → ".join(
            ["Warehouse"]
            + optimized_route
            + ["Warehouse"]
        )

        st.markdown(
            f"### 🚚 {vehicle_id}"
        )

        route_col1, route_col2 = (
            st.columns(2)
        )

        with route_col1:

            st.markdown(
                "**🔵 Initial Route**"
            )

            st.info(
                initial_text
            )

            st.write(
                f"Medicine Load: "
                f"{route_data['initial_load']}"
            )

            st.write(
                f"Late Minutes: "
                f"{route_data['initial_late']:.2f}"
            )

        with route_col2:

            st.markdown(
                "**🟢 Optimized Route**"
            )

            st.success(
                optimized_text
            )

            st.write(
                f"Medicine Load: "
                f"{route_data['optimized_load']}"
            )

            st.write(
                f"Late Minutes: "
                f"{route_data['optimized_late']:.2f}"
            )


    # --------------------------------------------------------
    # Route Comparison Table
    # --------------------------------------------------------

    st.subheader(
        "📋 Route Comparison Table"
    )

    route_table = []

    for route_data in (
        comparison[
            "route_comparison"
        ]
    ):

        route_table.append(
            {
                "Vehicle":
                    route_data[
                        "vehicle"
                    ],

                "Initial Chemist Order":
                    " → ".join(
                        route_data[
                            "initial_route"
                        ]
                    ),

                "Optimized Chemist Order":
                    " → ".join(
                        route_data[
                            "optimized_route"
                        ]
                    ),

                "Initial Load":
                    route_data[
                        "initial_load"
                    ],

                "Optimized Load":
                    route_data[
                        "optimized_load"
                    ],

                "Initial Late Minutes":
                    round(
                        route_data[
                            "initial_late"
                        ],
                        2
                    ),

                "Optimized Late Minutes":
                    round(
                        route_data[
                            "optimized_late"
                        ],
                        2
                    )
            }
        )

    st.dataframe(
        route_table,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Explanation
    # --------------------------------------------------------

    st.subheader(
        "💡 What Did the Algorithm Optimize?"
    )

    st.write(
        "The initial solution represents a random "
        "assignment and visiting order of the chemists."
    )

    st.write(
        "The Evolutionary Algorithm improves these "
        "routes through selection, crossover and "
        "mutation."
    )

    st.write(
        "The optimized solution aims to reduce total "
        "travel distance while minimizing capacity "
        "violations and delivery delays."
    )

    st.success(
        "The optimized route above shows the final "
        "chemist visiting order selected by the "
        "Evolutionary Algorithm."
    )


# --------------------------------------------------------
# Multiple Test Case Evaluation
# --------------------------------------------------------

st.divider()

st.header("🧪 Multiple Test Case Evaluation")

st.write(
    "The algorithm can also be evaluated under "
    "different delivery conditions."
)

run_tests = st.button(
    "🧪 RUN ALL TEST CASES",
    use_container_width=True
)

if run_tests:

    with st.spinner(
        "Running multiple test cases..."
    ):

        test_results = run_test_cases(
            warehouse=WAREHOUSE,
            vehicles=VEHICLES,
            chemists=CHEMISTS,

            population_size=population_size,
            generations=generations,

            mutation_rate=mutation_rate,
            crossover_rate=crossover_rate,

            tournament_size=tournament_size
        )

    st.success(
        "All test cases completed."
    )

    st.dataframe(
        test_results,
        use_container_width=True,
        hide_index=True
    )

# ========================================================
# PROJECT SUMMARY
# ========================================================

st.header(
        "📌 Project Summary"
    )

st.write(
        "This system demonstrates how an Evolutionary "
        "Algorithm can optimize pharmaceutical delivery "
        "routes by considering multiple vehicles, chemist "
        "demands, delivery time windows and travel distance."
    )

st.write(
        "The implementation uses population initialization, "
        "tournament selection, order crossover, swap mutation "
        "and a penalty-based fitness function."
    )
