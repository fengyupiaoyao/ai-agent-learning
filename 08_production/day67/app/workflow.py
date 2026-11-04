from app.checkpoint import CheckpointStore
from app.services import MockOrderService


class OrderWorkflow:
    def __init__(self, store, service):
        self.store = store
        self.service = service

    def initial_state(self, task_id):
        return {
            "task_id": task_id,
            "status": "pending",
            "completed_steps": [],
            "order_id": f"order-{task_id}",
            "payment_id": f"payment-{task_id}",
            "compensated_steps": [],
            "error": None,
        }

    def save(self, task_id, state):
        self.store.save(task_id, state)
        print(f"Saved state for {task_id}")

    def compensate(self, state):
        task_id = state["task_id"]
        order_id = state["order_id"]
        payment_id = state["payment_id"]

        state["status"] = "compensating"
        self.save(task_id, state)

        if (
            "charge_payment" in state["completed_steps"]
            and "refund_payment" not in state["completed_steps"]
        ):
            self.service.refund_payment(payment_id)
            state["compensated_steps"].append("refund_payment")
            self.save(task_id, state)

        # 再取消订单
        if (
            "create_order" in state["completed_steps"]
            and "cancel_order" not in state["compensated_steps"]
        ):
            self.service.cancel_order(order_id)
            state["compensated_steps"].append("cancel_order")
            self.save(task_id, state)

        state["status"] = "compensated"
        self.save(task_id, state)

        return state

    def run(self, task_id, fail_reserve=False):
        state = self.store.load(task_id)

        if state is None:
            state = self.initial_state(task_id)
            self.save(task_id, state)

        if state["status"] in ("completed", "compensated"):
            return state

        try:
            state["status"] = "running"
            self.save(task_id, state)

            # 2. 创建订单
            if "create_order" not in state["completed_steps"]:
                self.service.create_order(state["order_id"])
                state["completed_steps"].append("create_order")
                self.save(task_id, state)

            # 3. 扣款
            if "charge_payment" not in state["completed_steps"]:
                self.service.charge_payment(state["payment_id"])
                state["completed_steps"].append("charge_payment")
                self.save(task_id, state)

            # 4. 预留库存
            if "reserve_inventory" not in state["completed_steps"]:
                self.service.reserve_inventory(
                    state["order_id"],
                    should_fail=fail_reserve,
                )
                state["completed_steps"].append("reserve_inventory")
                self.save(task_id, state)

            # 5. 工作流完成
            state["status"] = "completed"
            self.save(task_id, state)

            return state
        except Exception as exc:
            state["error"] = str(exc)
            self.save(task_id, state)

            # 6. 失败后执行补偿
            return self.compensate(state)
