# Pharmaceutical Delivery Route Optimizer

A complete Soft Computing project that optimizes pharmaceutical delivery routes using a custom Evolutionary Algorithm.

## Features
- Multiple vehicles and chemists
- Vehicle capacity constraints
- Chemist delivery time windows
- Euclidean travel-distance calculation
- Penalty-based fitness function
- Tournament selection
- Order crossover
- Swap mutation
- Capacity repair
- Elitism
- Initial vs optimized route comparison
- Travel-time comparison (10 minutes per distance unit)
- Fitness convergence graph
- Multiple test-case evaluation
- High-demand infeasible test case

## Project structure
```text
pharmaceutical-route-optimizer/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── __init__.py
│   └── sample_data.py
├── algorithm/
│   ├── __init__.py
│   ├── evolutionary_algorithm.py
│   ├── fitness.py
│   ├── testing.py
│   └── baseline.py
└── utils/
    ├── __init__.py
    └── distance.py
```

## Run
Open a terminal in this folder and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Important
The main application uses the original Evolutionary Algorithm implementation. `baseline.py` is included as a separate compatibility/experimental module and is not imported by the main Evolutionary Algorithm.
