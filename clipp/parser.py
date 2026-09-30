from dataclasses import dataclass
from pathlib import Path


@dataclass
class Street:
    id: int
    a: int
    b: int
    direction: int
    time: int
    length: int
    category: str
    requirement: int


@dataclass
class Instance:
    num_junctions: int
    num_streets: int
    max_time: int
    num_vehicles: int
    depot: int
    water_waste_penalty: float
    streets: list[Street]
    vehicle_types: list[str]


def parse_instance(path: str | Path) -> Instance:

    with open(path, encoding="utf-8") as source:
        try:
            n, m, t, c, s, w = source.readline().split()
            n, m, t, c, s = map(int, (n, m, t, c, s))
            w = float(w)
        except ValueError as exc:
            raise ValueError("Invalid header: expected N M T C S W") from exc

        streets = []
        for street_id in range(m):
            try:
                a, b, d, time, length, category, requirement = (
                    source.readline().split()
                )
                streets.append(Street(
                    id=street_id,
                    a=int(a),
                    b=int(b),
                    direction=int(d),
                    time=int(time),
                    length=int(length),
                    category=category,
                    requirement=int(requirement),
                ))
            except ValueError as exc:
                raise ValueError(
                    f"Invalid street record on line {street_id + 2}"
                ) from exc

        vehicle_line = source.readline()
        vehicle_types = vehicle_line.split()
        if not vehicle_line or len(vehicle_types) != c:
            raise ValueError(f"Expected a final line with {c} vehicle types")

    return Instance(n, m, t, c, s, w, streets, vehicle_types)
