from app.checkpoint import CheckpointStore
from app.services import MockOrderService
from app.workflow import OrderWorkflow


def main():
    store = CheckpointStore()

    service = MockOrderService()

    workflow = OrderWorkflow(store, service)

    task_id = "task-001"

    print("开始执行订单工作流")

    result = workflow.run(
        task_id=task_id,
        fail_reserve=False,
    )

    print("\n最终状态：")
    print(result)

    print("\n业务操作记录：")
    for item in service.call_log:
        print(item)


if __name__ == "__main__":
    main()
