class MockOrderService:
    def __init__(self):
        self.orders = {}
        self.payments = {}
        self.inventory = {}
        self.refunds = set()
        self.cancelled_orders = set()

        self.call_log = []

    def create_order(self, order_id):
        if order_id not in self.orders:
            self.orders[order_id] = "created"
            self.call_log.append(f"create_order({order_id})")

        return order_id

    def charge_payment(self, payment_id):
        if payment_id not in self.payments:
            self.payments[payment_id] = "paid"
            self.call_log.append(f"charge_payment({payment_id})")

        return payment_id

    def reserve_inventory(self, order_id, should_fail=False):
        if should_fail:
            raise Exception("Inventory reservation failed")

        if order_id not in self.inventory:
            self.inventory[order_id] = "reserved"
            self.call_log.append(f"reserve_inventory({order_id})")

    def refund_payment(self, payment_id):
        if payment_id not in self.refunds:
            self.refunds.add(payment_id)
            self.payments[payment_id] = "refunded"
            self.call_log.append(f"refund_payment({payment_id})")

    def cancel_order(self, order_id):
        if order_id not in self.cancelled_orders:
            self.cancelled_orders.add(order_id)
            self.orders[order_id] = "cancelled"
            self.call_log.append(f"cancel_order({order_id})")
