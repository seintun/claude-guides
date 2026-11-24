---
type: index
repo: shop
commit: no git
date: 2026-11-23
---
# shop: repo map

Start with [[architecture]]. Ask questions against this map; open questions are under Questions.

## Components
- [[api]]: accepts orders and queues receipt jobs
- [[worker]]: sends receipts in the background
- [[shared]]: data types used by both

## Terms
- [[Order]]: a customer's request to buy items
- [[Receipt]]: the confirmation sent after an order
- [[Customer]]: who places an order

## Decisions
- [[queue-between-api-and-worker]]: receipts go through a queue, not a direct call

## Flows
- [[place-an-order]]: from the API call to the receipt job

## Questions
- [[which-broker]]: which message broker carries receipt jobs
- [[who-owns-services]]: who owns each component
