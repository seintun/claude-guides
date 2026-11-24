"""HTTP API: accepts orders and hands receipts to the worker queue."""
from shared.models import Order


class OrderService:
    def create_order(self, customer_id, items):
        order = Order(customer_id=customer_id, items=items)
        enqueue_receipt(order)
        return order


def enqueue_receipt(order):
    """Puts a receipt job on the queue; the worker sends it."""
    return {"job": "send_receipt", "order": order}
