"""Background jobs. Never imports from api/."""


def send_receipt(job):
    return f"receipt for {job['order']}"
