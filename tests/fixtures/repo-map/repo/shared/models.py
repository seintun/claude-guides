"""Data types shared by the API and the worker. No I/O here."""
from dataclasses import dataclass, field


@dataclass
class Order:
    customer_id: str
    items: list = field(default_factory=list)


@dataclass
class Customer:
    customer_id: str
