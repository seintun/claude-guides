---
type: component
kind: job
path: worker/
owner: UNKNOWN
depends_on: ["[[shared]]"]
provides: receipt jobs
key_names: [send_receipt]
---
# worker

## What
Runs background jobs such as sending a [[Receipt]].

## Why
UNKNOWN beyond [[queue-between-api-and-worker]].

## Boundaries and invariants
Nothing here imports from `api/`.
