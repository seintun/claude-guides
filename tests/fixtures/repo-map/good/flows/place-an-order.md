---
type: flow
entry: api/server.py
components: ["[[api]]", "[[worker]]"]
---
# Place an order

1. `OrderService.create_order` builds an `Order` (from [[shared]]).
2. `enqueue_receipt` puts a job on the queue.
3. [[worker]] runs `send_receipt` for the job.
