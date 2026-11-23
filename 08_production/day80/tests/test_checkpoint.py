from app.checkpoint import save_checkpoint, load_checkpoint


def test_checkpoint_save_and_load():
    state = {
        "task_id": "test-003",
        "status": "waiting_approval",
        "current_step": 2,
        "results": [],
    }

    save_checkpoint("test-003", state)

    loaded = load_checkpoint("test-003")

    assert loaded is not None
    assert loaded["status"] == "waiting_approval"
    assert loaded["current_step"] == 2
