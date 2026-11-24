---
type: decision
status: inferred
source: api/server.py
---
# Receipts go through a queue, not a direct call

## Context
Creating an order should not wait for a receipt to be sent.

## Decision
[[api]] builds a job with `enqueue_receipt`; [[worker]] runs `send_receipt`.

## Why
Inferred from the code: no ADR or commit message says so. See [[which-broker]].

## Consequences
The worker can fail or lag without failing the order.
