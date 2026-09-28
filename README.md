# Street Cleaning Optimization

This repository is being developed for an Advanced Algorithms course project on a **Street Cleaning Optimization Problem** based on graph-routing and coverage algorithms.

The goal is to find efficient routes for a fleet of street-cleaning vehicles while considering operational constraints such as time, street priority, vehicle capabilities, and available resources.

The project is designed to work with different street networks and should not depend on a specific city. A city is represented as input data, allowing the same algorithms to be tested on small networks as well as large urban areas.

## Problem Overview

A city is represented as a graph:

- **Vertices** represent street intersections.
- **Edges** represent streets.
- Streets may be one-way or bidirectional.
- Streets may have different traversal times, lengths, and cleaning requirements.
- Vehicles start from a common depot and return to the depot after completing their route.

Streets can have different roles:

- **Mandatory streets** must be cleaned.
- **Optional streets** provide additional value when cleaned.
- **Connector streets** are used for movement through the network but do not directly contribute to the cleaning objective.

The fleet may contain different vehicle types with different capabilities and resource limitations.

The main objective is to generate routes that satisfy the required constraints while maximizing useful street coverage and minimizing unnecessary travel and resource usage.

The problem is computationally difficult and is intended to be approached using graph algorithms, heuristics, approximation methods, and other optimization techniques.

## Project Structure

```text
street-cleaning/
|
├── README.md
├── .gitignore
|
├── src/
|   ├── algorithms/
|   ├── graph/
|   └── main.py
|
├── visualization/
|   ├── src/
|   ├── public/
|   └── package.json
|
├── data/
|   ├── input/
|   └── output/
|
├── tests/
|
└── docs/
```

### `src/`

Contains the core implementation of the project.

### `src/graph/`

Contains the graph representation of the street network.

This includes:

- Intersections
- Streets
- Direction of travel
- Distance
- Traversal time
- Street type and requirements

### `src/algorithms/`

Contains the algorithms used to generate and optimize cleaning routes.

Different approaches can be implemented independently and compared against each other.

### `visualization/`

Contains the Three.js application used to visualize the street network and calculated routes.

The visualization is kept separate from the routing and optimization logic.

```text
City Data
    ↓
Graph
    ↓
Algorithms
    ↓
Routes / Results
    ↓
Visualization
```

### `data/`

Contains input datasets and generated results.

```text
data/input/
```

Contains city and street-network datasets.

Different cities or generated graph instances can be stored independently.

Example:

```text
data/input/
├── small-city/
├── medium-city/
└── large-city/
```

```text
data/output/
```

Contains generated routes and algorithm results.

### `tests/`

Contains tests for the graph model, algorithms, constraints, and route calculations.

### `docs/`

Contains project documentation, problem definitions, algorithm notes, complexity analysis, and experiment results.

## Scalability

The project should support different graph sizes without being designed around one specific city.

Algorithms can therefore be evaluated using:

- Small test graphs
- Medium-sized city networks
- Large city networks

This allows different approaches to be compared in terms of:

- Solution quality
- Total distance
- Street coverage
- Resource usage
- Execution time
- Scalability

## Git Workflow

The `main` branch contains the stable version of the project.

Do not work directly on `main`.

Before starting new work:

```bash
git checkout main
git pull
```

Create a branch for your task:

```bash
git checkout -b feature/your-feature-name
```

Examples:

```text
feature/graph-model
feature/routing-algorithm
feature/fleet-model
feature/threejs-visualization
feature/city-data-import
```

After finishing your work:

```bash
git add .
git commit -m "feat: add graph model"
git push -u origin feature/your-feature-name
```

Then create a Pull Request or Merge Request:

```text
feature/your-feature-name
        ↓
       main
```

Changes should be reviewed before being merged.

## Git Rules

- Do not push directly to `main`.
- Create one branch per task or feature.
- Pull the latest `main` before starting new work.
- Keep commits clear and focused.
- Create a Pull Request or Merge Request when the work is ready.
- Delete the branch after it has been merged.
