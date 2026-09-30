from dataclasses import dataclass
from heapq import heappop, heappush

from .parser import Instance


@dataclass(frozen=True)
class Edge:
    destination: int
    street_id: int
    time: int


@dataclass
class Path:
    junctions: list[int]
    street_ids: list[int]
    total_time: int


Adjacency = list[list[Edge]]


def build_graph(instance: Instance) -> Adjacency:

    graph: Adjacency = [[] for _ in range(instance.num_junctions)]
    for street in instance.streets:
        graph[street.a].append(Edge(street.b, street.id, street.time))
        if street.direction == 2:
            graph[street.b].append(Edge(street.a, street.id, street.time))
    for edges in graph:
        edges.sort(key=lambda edge: (edge.street_id, edge.destination))
    return graph


def shortest_path(graph: Adjacency, start: int, destination: int) -> Path | None:

    if start == destination:
        return Path([start], [], 0)

    distances = {start: 0}
    previous: dict[int, tuple[int, int]] = {}
    queue = [(0, start)]

    while queue:
        elapsed, junction = heappop(queue)
        if elapsed != distances[junction]:
            continue
        if junction == destination:
            junctions = [destination]
            street_ids = []
            while junction != start:
                junction, street_id = previous[junction]
                junctions.append(junction)
                street_ids.append(street_id)
            return Path(junctions[::-1], street_ids[::-1], elapsed)

        for edge in graph[junction]:
            candidate = elapsed + edge.time
            best = distances.get(edge.destination)
            if best is None or candidate < best:
                distances[edge.destination] = candidate
                previous[edge.destination] = (junction, edge.street_id)
                heappush(queue, (candidate, edge.destination))

    return None
