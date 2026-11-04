from app.checkpoint import CheckpointStore
from app.services import MockOrderService
from app.workflow import OrderWorkflow


def test_failure_triggers_compensation(tmp_path):
    store = CheckpointStore(tmp_path)
    service = MockOrderService()
    workflow = OrderWorkflow(store, service)

    result = workflow.run("test-001", fail_reserve=True)

    assert result["status"] == "compensated"

    assert "create_order" in result["completed_steps"]
    assert "charge_payment" in result["completed_steps"]

    assert "refund_payment" in result["compensated_steps"]
    assert "cancel_order" in result["compensated_steps"]

    assert service.payments["payment-test-001"] == "refunded"
    assert service.orders["order-test-001"] == "cancelled"


def test_checkpoint_can_be_loaded_after_restart(tmp_path):
    store = CheckpointStore(tmp_path)
    service = MockOrderService()

    workflow = OrderWorkflow(store, service)

    # 第一次执行：库存失败，发生补偿
    workflow.run("test-002", fail_reserve=True)

    # 模拟重新创建工作流对象
    new_workflow = OrderWorkflow(
        CheckpointStore(tmp_path),
        service,
    )

    result = new_workflow.run("test-002")

    assert result["status"] == "compensated"

    # 不应该再次退款或取消订单
    assert service.call_log.count("refund_payment(payment-test-002)") == 1
    assert service.call_log.count("cancel_order(order-test-002)") == 1


def test_successful_workflow(tmp_path):
    store = CheckpointStore(tmp_path)
    service = MockOrderService()
    workflow = OrderWorkflow(store, service)

    result = workflow.run("test-003")

    assert result["status"] == "completed"
    assert len(result["completed_steps"]) == 3
    assert result["compensated_steps"] == []
