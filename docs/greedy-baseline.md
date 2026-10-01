# Greedy baseline

Mandatory streets are processed in requirement groups 30, 20, then 10.
Within each group, choose the feasible street/vehicle/orientation candidate with
the smallest (incremental traversal time, street ID, vehicle ID, start, end).
Feasibility includes a shortest return to the depot. Actual returns are appended
after all mandatory streets have been assigned.

After returning to the depot, compatible optional streets already traversed are
cleaned once, preferring lower capacity then vehicle ID. This adds no movement.
The algorithm is deterministic; failure does not prove the instance infeasible.

Inputs contain the header, street records, and vehicle types, with no coordinates.
The output declares traversal count n, then n+1 junction IDs, then cleaned street
IDs for each vehicle. This follows the external validator's format.

Official score is alpha * coverage + (1-alpha) * efficiency. Coverage normalizes
distinct cleaned length by all mandatory/optional length; efficiency normalizes
water waste. The parser's historical `water_waste_penalty` field holds alpha.
For instance_E, alpha=1 and the accepted score is 0.58363268951526.

The layout migration does not change algorithms, scoring, or route assignments.
