---
type: component
kind: service
path: api/
owner: UNKNOWN
depends_on: ["[[shared]]"]
provides: orders API
key_names: [OrderService, create_order, enqueue_receipt]
---
# api

## What
Accepts orders and puts a receipt job on the queue. Entry point: `api/server.py`.

## Why
Receipts are slow, so they leave the request path: [[queue-between-api-and-worker]].

## Boundaries and invariants
Talks to [[worker]] only through the queue. Owner is UNKNOWN: [[who-owns-services]].
