from dataclasses import dataclass, field

from .graph import build_graph, shortest_path
from .parser import Instance


VEHICLE_CAPACITIES = {"S": 10, "M": 20, "L": 30}


@dataclass
class VehicleRoute:
    vehicle_id: int
    vehicle_type: str
    capacity: int
    current_junction: int
    junctions: list[int]
    total_time: int = 0
    street_ids: list[int] = field(default_factory=list)
    cleaned_street_ids: list[int] = field(default_factory=list)


@dataclass
class Solution:
    routes: list[VehicleRoute]


class GreedyAssignmentError(ValueError):

    def __init__(self, street_id: int, partial_solution: Solution,
                 reasons: list[str]) -> None:
        super().__init__(
            f"Greedy assignment failed for mandatory street {street_id}: "
            "no feasible vehicle and orientation"
        )
        self.street_id = street_id
        self.partial_solution = partial_solution
        self.reasons = reasons


def solve(instance: Instance) -> Solution:

    graph = build_graph(instance)
    routes = [
        VehicleRoute(
            vehicle_id=vehicle_id,
            vehicle_type=vehicle_type,
            capacity=VEHICLE_CAPACITIES[vehicle_type],
            current_junction=instance.depot,
            junctions=[instance.depot],
        )
        for vehicle_id, vehicle_type in enumerate(instance.vehicle_types)
    ]
    mandatory = sorted(
        (street for street in instance.streets if street.category == "M"),
        key=lambda street: (-street.requirement, street.id),
    )

    for requirement in sorted({s.requirement for s in mandatory}, reverse=True):
        remaining = [s for s in mandatory if s.requirement == requirement]
        while remaining:
            best_key = None
            best_candidate = None
            reasons = []
            for street in remaining:
                orientations = [(street.a, street.b)]
                if street.direction == 2:
                    orientations.append((street.b, street.a))

                for route in routes:
                    if route.capacity < street.requirement:
                        reasons.append(
                            f"Street {street.id}, vehicle {route.vehicle_id}: capacity {route.capacity} "
                            f"< requirement {street.requirement}"
                        )
                        continue
                    for start, end in orientations:
                        label = f"Street {street.id}, vehicle {route.vehicle_id}, {start}->{end}"
                        approach = shortest_path(graph, route.current_junction, start)
                        if approach is None:
                            reasons.append(f"{label}: street start unreachable")
                            continue
                        return_path = shortest_path(graph, end, instance.depot)
                        if return_path is None:
                            reasons.append(f"{label}: depot unreachable after cleaning")
                            continue
                        incremental_time = approach.total_time + street.time
                        if (route.total_time + incremental_time + return_path.total_time
                                > instance.max_time):
                            reasons.append(
                                f"{label}: {route.total_time} committed + "
                                f"{approach.total_time} approach + {street.time} street + "
                                f"{return_path.total_time} return = "
                                f"{route.total_time + incremental_time + return_path.total_time} "
                                f"> limit {instance.max_time}"
                            )
                            continue

                        key = (incremental_time, street.id, route.vehicle_id, start, end)
                        if best_key is None or key < best_key:
                            best_key = key
                            best_candidate = (street, route, approach, end)


            if best_candidate is None:
                reasons.insert(0, f"No feasible candidate in requirement {requirement}; "
                               f"remaining streets: {[s.id for s in remaining]}")
                raise GreedyAssignmentError(remaining[0].id, Solution(routes), reasons)

            street, route, approach, end = best_candidate
            route.junctions.extend(approach.junctions[1:])
            route.street_ids.extend(approach.street_ids)
            route.junctions.append(end)
            route.street_ids.append(street.id)
            route.total_time += approach.total_time + street.time
            route.current_junction = end
            route.cleaned_street_ids.append(street.id)
            remaining.remove(street)

    for route in routes:
        return_path = shortest_path(graph, route.current_junction, instance.depot)
        if return_path is None:
            raise ValueError(f"Vehicle {route.vehicle_id} cannot return to depot")
        route.junctions.extend(return_path.junctions[1:])
        route.street_ids.extend(return_path.street_ids)
        route.total_time += return_path.total_time
        route.current_junction = instance.depot

    streets_by_id = {street.id: street for street in instance.streets}
    cleaned = {street_id for route in routes for street_id in route.cleaned_street_ids}
    for route in sorted(routes, key=lambda route: (route.capacity, route.vehicle_id)):
        for street_id in sorted(set(route.street_ids)):
            street = streets_by_id[street_id]
            if (street.category == "O" and route.capacity >= street.requirement
                    and street_id not in cleaned):
                route.cleaned_street_ids.append(street_id)
                cleaned.add(street_id)

    return Solution(routes)
