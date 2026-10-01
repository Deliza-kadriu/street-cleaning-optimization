from pathlib import Path

from .solver import Solution


def write_solution(solution: Solution, path: str | Path) -> None:

    lines = [str(len(solution.routes))]
    for route in solution.routes:
        declared_step_count = len(route.street_ids)
        if len(route.junctions) != declared_step_count + 1:
            raise ValueError(
                f"Vehicle {route.vehicle_id}: {len(route.junctions)} junctions "
                f"do not match {len(route.street_ids)} traversed streets + 1"
            )
        junction_line = " ".join(map(str, route.junctions))
        if not (declared_step_count + 1 == len(route.junctions)
                == len(junction_line.split())):
            raise ValueError(f"Vehicle {route.vehicle_id}: serialized node count mismatch")
        lines.extend([
            str(declared_step_count),
            junction_line,
            " ".join(map(str, route.cleaned_street_ids)),
        ])
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
