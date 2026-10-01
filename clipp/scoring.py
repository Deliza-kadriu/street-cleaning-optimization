from dataclasses import dataclass

from .parser import Instance
from .solver import Solution, VEHICLE_CAPACITIES
from .validator import validate_solution


@dataclass(frozen=True)
class Score:
    cleaned_length: int
    total_water_waste: float
    score: float
    coverage: float
    efficiency: float


def calculate_score(instance: Instance, solution: Solution) -> Score:

    errors = validate_solution(instance, solution)
    if errors:
        raise ValueError("Cannot score an invalid solution: " + "; ".join(errors))
    streets = {street.id: street for street in instance.streets}
    cleaned = set()
    waste = 0.0
    for vehicle_id, route in enumerate(solution.routes):
        capacity = VEHICLE_CAPACITIES[instance.vehicle_types[vehicle_id]]
        for street_id in route.cleaned_street_ids:
            street = streets[street_id]
            if street.category in {"M", "O"}:
                cleaned.add(street_id)
                waste += (capacity - street.requirement) * (street.length / 1000)
    length = sum(streets[street_id].length for street_id in sorted(cleaned))
    eligible = [street for street in instance.streets if street.category in {"M", "O"}]
    max_length = sum(street.length for street in eligible)
    max_waste = sum((30 - street.requirement) * (street.length / 1000)
                    for street in eligible)
    coverage = length / max_length if max_length > 0 else 0.0
    efficiency = 1.0 - waste / max_waste if max_waste > 0 else 1.0
    alpha = instance.water_waste_penalty
    value = alpha * coverage + (1.0 - alpha) * efficiency
    return Score(length, waste, value, coverage, efficiency)
