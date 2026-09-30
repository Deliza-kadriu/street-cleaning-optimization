from .parser import Instance
from .solver import Solution, VEHICLE_CAPACITIES


def validate_solution(instance: Instance, solution: Solution) -> list[str]:

    errors: list[str] = []
    streets = {street.id: street for street in instance.streets}
    cleaned = set()
    if len(solution.routes) != instance.num_vehicles:
        errors.append(f"Expected {instance.num_vehicles} vehicle routes, "
                      f"got {len(solution.routes)}")

    for vehicle_id, route in enumerate(solution.routes):
        label = f"Vehicle {vehicle_id}"
        if vehicle_id >= len(instance.vehicle_types):
            errors.append(f"{label}: no such vehicle in instance")
            continue
        vehicle_type = instance.vehicle_types[vehicle_id]
        capacity = VEHICLE_CAPACITIES[vehicle_type]
        if route.vehicle_id != vehicle_id:
            errors.append(f"{label}: incorrect vehicle ID {route.vehicle_id}")
        if route.vehicle_type != vehicle_type or route.capacity != capacity:
            errors.append(f"{label}: vehicle type or capacity differs from instance")
        if not route.junctions:
            errors.append(f"{label}: empty junction route")
        else:
            if route.junctions[0] != instance.depot:
                errors.append(f"{label}: route does not start at depot")
            if route.junctions[-1] != instance.depot:
                errors.append(f"{label}: route does not end at depot")
            if route.current_junction != route.junctions[-1]:
                errors.append(f"{label}: current junction differs from route end")
        for junction in route.junctions:
            if not 0 <= junction < instance.num_junctions:
                errors.append(f"{label}: invalid junction ID {junction}")
        if len(route.street_ids) != max(0, len(route.junctions) - 1):
            errors.append(f"{label}: street count does not match route steps")

        total_time = 0
        traversed = set()
        for step, street_id in enumerate(route.street_ids):
            street = streets.get(street_id)
            if street is None:
                errors.append(f"{label}: invalid traversed street ID {street_id}")
                continue
            total_time += street.time
            if step + 1 >= len(route.junctions):
                continue
            a, b = route.junctions[step:step + 2]
            legal = (a, b) == (street.a, street.b) or (
                street.direction == 2 and (a, b) == (street.b, street.a)
            )
            if not legal:
                errors.append(f"{label}: illegal traversal of street {street_id} "
                              f"at step {step}: {a}->{b}")
            else:
                traversed.add(street_id)
        if total_time != route.total_time:
            errors.append(f"{label}: reported time {route.total_time} "
                          f"differs from traversal time {total_time}")
        if total_time > instance.max_time:
            errors.append(f"{label}: traversal time {total_time} "
                          f"> limit {instance.max_time}")

        for street_id in route.cleaned_street_ids:
            street = streets.get(street_id)
            if street is None:
                errors.append(f"{label}: invalid cleaned street ID {street_id}")
                continue
            if street_id not in traversed:
                errors.append(f"{label}: cleaned street {street_id} was not traversed")
            if capacity < street.requirement:
                errors.append(f"{label}: insufficient capacity for street {street_id}")
            if street.category == "C":
                errors.append(f"{label}: connector street {street_id} cannot be cleaned")
            cleaned.add(street_id)

    missing = sorted(street.id for street in instance.streets
                     if street.category == "M" and street.id not in cleaned)
    if missing:
        errors.append("Mandatory streets not cleaned: " + ", ".join(map(str, missing)))
    return errors
